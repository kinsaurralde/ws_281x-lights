import json
import time
import threading
import requests

BRIGHTNESS_BUFFER_TIMER = 0.01
GET_TIMEOUT = 0.3
POST_TIMEOUT = 0.5


class Controllers:
    """Handles sending requests to controllers"""

    def __init__(self, config, nosend, version_info, controller_module):
        self.version_info = version_info
        self.nosend = nosend
        self.send_counter = 0
        self.urls = {}
        self.inactive = {}
        self.disabled = {}
        self.latencies = {}
        self.last_brightness = {}
        self.brightness_queue = {}
        self.brightness_timer_active = False
        self.background_data = {}
        self.config = {}
        self.controller_module = controller_module
        self.controllers = {}
        self.alias = config.get("alias", {})
        self._setupConfig(config["controllers"])
        self.updateControllerLatencies()

    def setNoSend(self, value: bool):
        """Set nosend"""
        self.nosend = value

    def disableController(self, name: str) -> list:
        """Disable controller"""
        if name not in self.config:
            return [{"url": None, "id": name, "message": "Controller not found",}]
        url = self.config[name]["url"]
        if url in self.disabled:
            return [{"url": None, "id": name, "message": "Controller not enabled",}]
        if url not in self.disabled:
            self.disabled[url] = []
        if name not in self.disabled[url]:
            self.disabled[url].append(name)
        return []

    def enableController(self, name: str) -> list:
        """Enable controller"""
        if name not in self.config:
            return [{"url": None, "id": name, "message": "Controller not found",}]
        url = self.config[name]["url"]
        if url not in self.disabled:
            return [{"url": None, "id": name, "message": "Controller not disabled",}]
        self.disabled.pop(url)
        self._initController(url, self.config[name])
        return []

    def updateControllerLatencies(self, background=None):
        """Redetermine latency to controllers"""
        if self.nosend:
            return
        for url in self.latencies:
            if url in self.disabled:
                self.latencies[url] = "disabled"
                continue
            start_time = time.time()
            if self._sending_thread([], url) is None:
                self.latencies[url] = None
            else:
                end_time = time.time()
                latency = float((end_time - start_time) * 1000)
                previous = self.latencies[url]
                if not isinstance(previous, float):
                    self.background_data[
                        "initialized"
                    ] = self.getControllerInitialized()
                    self.background_data["version"] = self.getControllerVersionInfo()
                    if background is not None and previous is None:
                        background.updateData()
                    previous = latency
                self.latencies[url] = (previous + latency) / 2
        print("Controller Latencies", self.latencies)

    def getControllerLatencies(self) -> dict:
        """Get controller latencies"""
        latency = {}
        for url in self.latencies:
            for controller in self.urls[url]:
                latency[controller] = self.latencies[url]
        return latency

    def getBackgroundData(self) -> dict:
        """Get background data"""
        data = self.background_data
        self.background_data = {}
        return data

    def getControllerVersionInfo(self) -> dict:
        """Get version info of controllers and webapp"""
        fails = []
        data = {}
        version_match = True
        hash_match = True
        for url in self.urls:
            if url in self.disabled:
                continue
            response = self._sending_thread(fails, url + "/versioninfo")
            if response is None:
                continue
            response = response.json()
            for controller in self.urls[url]:
                data[controller] = response
            if (
                response["major"] != self.version_info["major"]
                or response["minor"] != self.version_info["minor"]
                or response["patch"] != self.version_info["patch"]
            ):
                version_match = False
                fails.append(
                    {"url": url, "id": "version", "message": "Version doesnt match"}
                )
            if (
                response["esp_hash"] != self.version_info["esp_hash"]
                or response["rpi_hash"] != self.version_info["rpi_hash"]
            ):
                hash_match = False
                fails.append({"url": url, "id": "hash", "message": "Hash doesnt match"})
        return {
            "versioninfo": data,
            "fails": fails,
            "webapp": self.version_info,
            "version_match": version_match,
            "hash_match": hash_match,
        }

    def getControllerSizes(self) -> dict:
        """Get number of leds on each controller"""
        result = {}
        for c in self.config:
            result[c] = self.config[c]["init"]["num_leds"]
        return result

    def getControllerInitialized(self) -> dict:
        """Get whether controllers are initialzied"""
        fails = []
        data = {}
        for url in self.urls:
            if url in self.disabled:
                continue
            response = self._sending_thread(fails, url + "/init")
            if response is None:
                continue
            response = response.json()
            for controller in self.config:
                if self.config[controller]["url"] == url:
                    response_index = int(self.config[controller]["strip_id"])
                    if response_index < 0 or response_index >= len(response):
                        fails.append(
                            {
                                "url": url,
                                "id": response_index,
                                "message": "Strip id does not exist on remote controller",
                            }
                        )
                    else:
                        data[controller] = response[response_index]
        return {"fails": fails, "initialized": data}

    def send(self, commands: list) -> list:
        """Send commands to controllers"""
        queue = {}
        fails = []
        commands = self._replaceSendAlias(commands)
        for command in commands:
            controller_name = command["id"]
            if controller_name not in self.config:
                fails.append(
                    {
                        "url": "localhost",
                        "id": controller_name,
                        "message": "Controller not found",
                    }
                )
                continue
            command["id"] = self.config[controller_name]["strip_id"]
            url = self.config[controller_name]["url"]
            if url in self.disabled:
                continue
            if url not in queue:
                queue[url] = []
            queue[url].append(command)
        threads = []
        for url in queue:
            threads.append(
                self._send(fails, url + "/data", queue[url], queue[url][0]["id"])
            )
            if url in self.controllers:
                self.controllers[url].handleData(queue[url])
        for thread in threads:
            thread.join()
        if self.send_counter % 25 == 0:  # pragma: no cover
            self.updateControllerLatencies()
        return fails

    def getConfig(self) -> dict:
        """"Get controller config"""
        return self.config

    def getLastBrightness(self) -> int:
        """Get last_brightness"""
        return self.last_brightness

    def brightness(self, requests: list):
        """Change brightness of controllers"""
        for request in requests:
            name = request["name"]
            if name not in self.config:
                continue
            value = request["value"]
            url = self.config[name]["url"]
            if url in self.disabled:
                continue
            self.brightness_queue[name] = (
                url + f"/brightness?value={value}&id={self.config[name]['strip_id']}"
            )
            self.last_brightness[name] = value
            if not self.brightness_timer_active:
                self.brightness_timer_active = True
                thread = threading.Thread(target=self._brightness())
                thread.start()

    def getPixels(self) -> dict:
        """Get current pixels (simulated)"""
        result = {}
        for i in self.controllers:
            pixels = self.controllers[i].getPixels()
            for j in range(min(len(self.urls[i]), len(pixels))):
                result[self.urls[i][j]] = pixels[j]
        return result

    def _setupConfig(self, controllers):
        id_counter = 0
        self.config = {}
        for controller in controllers:
            name = controller["name"]
            if not controller["active"]:
                continue
            self.config[name] = controller
            url = controller["url"]
            self.latencies[url] = None
            if url not in self.urls:
                self.urls[url] = []
                if self.controller_module is not None:
                    self.controllers[url] = self.controller_module.NeoPixels()
            self.urls[url].append(name)
            if controller["active"] == "disabled":
                self.disableController(name)
            self._initController(url, controller)
            controller["id"] = id_counter

    def _initController(self, url: str, controller: dict):
        if url in self.disabled:
            return
        self.last_brightness[controller["name"]] = controller["init"]["brightness"]
        self._send(
            [],
            url + "/init",
            {"id": controller["strip_id"], "init": controller["init"]},
        )
        if url in self.controllers:
            self.controllers[url].init(
                {"id": controller["strip_id"], "init": controller["init"]}
            )

    def _send(
        self, fails: list, url: str, payload: dict = None, controller_id: str = None
    ):
        thread = threading.Thread(
            target=self._sending_thread, args=(fails, url, payload, controller_id)
        )
        thread.start()
        return thread

    def _sending_thread(
        self, fails: list, url: str, payload: dict = None, controller_id: str = None
    ) -> dict:
        self.send_counter += 1
        if self.nosend:
            fails.append(
                {"url": url, "id": controller_id, "message": "No send is true"}
            )
            return None
        try:
            if payload is None:
                return requests.get(url, timeout=GET_TIMEOUT)
            return requests.post(url, data=json.dumps(payload), timeout=POST_TIMEOUT)
        except requests.RequestException:
            print(f"Failed to send to {url}")
            fails.append(
                {"url": url, "id": controller_id, "message": "Connection Error"}
            )
        return None

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

    def _brightness(self):
        time.sleep(BRIGHTNESS_BUFFER_TIMER)
        while len(self.brightness_queue) > 0:
            name = list(self.brightness_queue.keys())[0]
            self._send([], self.brightness_queue[name])
            self.brightness_queue.pop(name)
        self.brightness_timer_active = False
