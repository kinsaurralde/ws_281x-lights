import time
import threading
import logging

from .manager import ControllerManager
from .extras import RequestResponse

BRIGHTNESS_BUFFER_TIMER = 0.01
GET_TIMEOUT = 0.3
POST_TIMEOUT = 0.5

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class Controllers:
    """Handles sending requests to controllers"""

    def __init__(self, config, nosend, version_info, socketio):
        self.version_info = version_info
        self.socketio = socketio
        self.nosend = nosend
        self.send_counter = 0
        self.urls = {}
        self.inactive = {}
        self.disabled = {}
        self.rtt = {}
        self.last_brightness = {}
        self.brightness_queue = {}
        self.brightness_timer_active = False
        self.background_data = {}
        self.controllers = {}
        self.alias = config.get("alias", {})
        self._setupConfig(config["controllers"])
        self.manager = ControllerManager(self)
        self._initControllers()
        self.updateControllerRTT()

    def setNoSend(self, value: bool):
        """Set nosend"""
        self.nosend = value
        self.manager.setNoSend(value)

    def disableController(self, name: str) -> list:
        """Disable controller"""
        if name not in self.controllers:
            return {"error": True, "id": name, "message": "Controller not found"}
        url = self.controllers[name]["url"]
        if url in self.disabled:
            return {"error": True, "id": name, "message": "Controller not enabled"}
        if url not in self.disabled:
            self.disabled[url] = []
        if name not in self.disabled[url]:
            self.disabled[url].append(name)
        return {"error": False, "id": name, "message": "Disabled controller"}

    def enableController(self, name: str) -> list:
        """Enable controller"""
        if name not in self.controllers:
            return {"error": True, "id": name, "message": "Controller not found"}
        url = self.controllers[name]["url"]
        if url not in self.disabled:
            return {"error": True, "id": name, "message": "Controller not disabled"}
        self.disabled.pop(url)
        self._initController(url, self.controllers[name])
        return {"error": False, "id": name, "message": "Enabled controller"}

    def updateControllerRTT(self):
        if self.nosend:
            return
        for url in self.rtt:
            if url in self.disabled:
                self.rtt[url] = False
                continue
            rtt = self.manager.getRTT(url)
            if self.rtt[url] is None and rtt is not None:
                self.updateControllerVersionInfo()
                self.updateControllerInitialized()
            self.rtt[url] = rtt
        return

    def getControllerRTT(self) -> dict:
        """Get controller latencies"""
        rtt = {}
        for url in self.rtt:
            for controller in self.urls[url]:
                rtt[controller] = self.rtt[url]
        return rtt

    def getBackgroundData(self) -> dict:
        """Get background data"""
        data = self.background_data
        self.background_data = {}
        return data

    def getControllerVersionInfo(self):
        return self.background_data.get("version", {})

    def getControllerInitialzed(self):
        return self.background_data.get("initialized", {})

    def checkVersionMatch(self, r) -> bool:
        v = self.version_info
        return v["major"] == r["major"] and v["minor"] == r["minor"] and v["patch"] == r["patch"]

    def checkHashMatch(self, r) -> bool:
        v = self.version_info
        return v["esp_hash"] == r["esp_hash"] and v["rpi_hash"] == r["rpi_hash"]

    def updateControllerVersionInfo(self) -> None:
        """Get version info of controllers and webapp"""
        data = {}
        version_match = True
        hash_match = True
        for url in self.urls:
            if url in self.disabled:
                continue
            response = self.manager.send(url, url, "/versioninfo")
            if not response.good:
                log.warning(f"Failed to get version info from {response.url}")
                continue
            response = response.response.json()
            for controller in self.urls[url]:
                data[controller] = response
            if not self.checkVersionMatch(response):
                version_match = False
            if not self.checkHashMatch(response):
                hash_match = False
        self.background_data["version"] = {
            "versioninfo": data,
            "webapp": self.version_info,
            "version_match": version_match,
            "hash_match": hash_match,
        }

    def getControllerSizes(self) -> dict:
        """Get number of leds on each controller"""
        result = {}
        for c in self.controllers:
            result[c] = self.controllers[c]["init"]["num_leds"]
        return result

    def updateControllerInitialized(self) -> None:
        """Get whether controllers are initialzied"""
        data = {}
        for url in self.urls:
            if url in self.disabled:
                continue
            response = self.manager.send(url, url, "/init")
            if not response.good:
                log.warning(f"Failed to get controller initialized from {response.url}")
                continue
            response = response.response.json()
            for controller in self.controllers:
                if self.controllers[controller]["url"] == url:
                    response_index = int(self.controllers[controller]["strip_id"])
                    if 0 <= response_index < len(response):
                        data[controller] = response[response_index]
        self.background_data["initialized"] = {"initialized": data}

    def send(self, commands: list) -> list:
        """Send commands to controllers"""
        commands = self._replaceSendAlias(commands)
        self.socketio.emit("handleData", commands)
        session_id = self.manager.startSession()
        for command in commands:
            controller_name = command["id"]
            url = self.getUrl(controller_name)
            if url is None:
                err_msg = f"Controller {controller_name} does not exist"
                log.error(err_msg)
                self.manager.addToSession(session_id, RequestResponse(None, err_msg, controller_id=controller_name))
                continue
            if url in self.disabled:
                log.info(f"Not sending to controller {controller_name} because it is disabled")
                continue
            command["id"] = self.controllers[controller_name]["strip_id"]
            self.manager.send(url, controller_name, "/data", "POST", [command], session_id, rtt_skip=True)
        return self.manager.endSession(session_id)

    def getConfig(self) -> dict:
        """"Get controller config"""
        return self.controllers

    def getLastBrightness(self) -> int:
        """Get last_brightness"""
        return self.last_brightness

    def brightness(self, requests: list):
        """Change brightness of controllers"""
        for request in requests:
            name = request["name"]
            if name not in self.controllers:
                continue
            value = request["value"]
            url = self.controllers[name]["url"]
            if url in self.disabled:
                continue
            self.brightness_queue[name] = url + f"/brightness?value={value}&id={self.controllers[name]['strip_id']}"
            self.last_brightness[name] = value
            if not self.brightness_timer_active:
                self.brightness_timer_active = True
                thread = threading.Thread(target=self._brightness())
                thread.start()

    def getPixels(self) -> dict:
        """Get current pixels (simulated)"""
        result = {}
        for url in self.urls:
            response = self.manager.send(url, url, "/getpixels")
            if not response.good:
                log.warning(f"Failed to get pixels from {response.url}")
                continue
            response = response.response.json()
        return result

    def _setupConfig(self, controllers):
        id_counter = 0
        self.controllers = {}
        for controller in controllers:
            name = controller["name"]
            if not controller["active"]:
                continue
            self.controllers[name] = controller
            url = controller["url"]
            self.rtt[url] = None
            if url not in self.urls:
                self.urls[url] = []
            self.urls[url].append(name)
            if controller["active"] == "disabled":
                self.disableController(name)
            controller["id"] = id_counter

    def _initControllers(self):
        session_id = self.manager.startSession()
        for controller in self.controllers:
            self._initController(controller, session_id)
        responses = self.manager.endSession(session_id)
        if not responses["all_good"]:
            for controller in responses["errors"]:
                log.error(
                    f"Failed to initialize controller {controller} because {responses['responses'][controller].message}"
                )

    def _initController(self, controller_id: str, session_id=0):
        url = self.getUrl(controller_id)
        if url is None:
            log.critical(
                f"Setup attempted to initialze controller {controller_id}"
                f"which does not exist in Controllers.controllers: {self.controllers}"
            )
            return
        if url in self.disabled:
            return
        controller = self.controllers[controller_id]
        self.last_brightness[controller["name"]] = controller["init"]["brightness"]
        init_values = {"id": controller["strip_id"], "init": controller["init"]}
        response = self.manager.send(url, controller_id, "/init", "POST", init_values, session_id)
        if not response.good:
            log.error(f"Failed to initialize controller {response.controller_id} because {response.message}")

    def _replaceSendAlias(self, commands: list) -> list:
        new_commands = []
        for command in commands:
            if "id" not in command:
                continue
            if command["id"] in self.alias:
                new_command = command.copy()
                for name in self.alias[command["id"]]:
                    new_command["id"] = name
                    new_commands.append(new_command.copy())
            else:
                new_commands.append(command)
        return new_commands

    def getUrl(self, controller_id: str) -> str:
        """Return url of controller id or None if controller_id does not exist

        Callers of this function should check for None response which means controller does not exist
        """
        # If controller_id is an alias, convert to acutal id
        if controller_id in self.alias:
            controller_id = self.alias[controller_id]
        # Return url if controller_id exists
        if controller_id in self.controllers:
            return self.controllers[controller_id]["url"]
        return None

    def _brightness(self):
        time.sleep(BRIGHTNESS_BUFFER_TIMER)
        while len(self.brightness_queue) > 0:
            name = list(self.brightness_queue.keys())[0]
            self.manager.send(self.brightness_queue[name], threaded=True)
            self.brightness_queue.pop(name)
        self.brightness_timer_active = False
