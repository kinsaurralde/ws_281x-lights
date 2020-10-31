import json
import time
import threading
import requests

BRIGHTNESS_BUFFER_TIMER = 0.01
GET_TIMEOUT = 0.3
POST_TIMEOUT = 0.5


class Controllers:
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
        self._setupConfig(config["controllers"])
        self.updateControllerLatencies()

    def _setupConfig(self, controllers):
        id_counter = 0
        self.config = {}
        for controller in controllers:
            self.config[controller["name"]] = controller
            url = controller["url"]
            self.latencies[url] = None
            if url not in self.urls:
                self.urls[url] = []
                if self.controller_module is not None:
                    self.controllers[url] = self.controller_module.NeoPixels()
            self.urls[url].append(controller["name"])
            if controller["active"] == "disabled":
                self.disableController(controller["name"])
            self.initController(url, controller)
            controller["id"] = id_counter
        print(self.controllers)

    def setNoSend(self, value):
        self.nosend = value

    def initController(self, url, controller):
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

    def _send(self, fails, url, payload=None, controller_id=None):
        thread = threading.Thread(
            target=self._sending_thread, args=(fails, url, payload, controller_id)
        )
        thread.start()
        return thread

    def _sending_thread(self, fails, url, payload=None, controller_id=None):
        self.send_counter += 1
        if self.nosend:
            print(f"Would have sent to {url}:\n{payload}")
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

    def disableController(self, name):
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

    def enableController(self, name):
        if name not in self.config:
            return [{"url": None, "id": name, "message": "Controller not found",}]
        url = self.config[name]["url"]
        if url not in self.disabled:
            return [{"url": None, "id": name, "message": "Controller not disabled",}]
        self.disabled.pop(url)
        self.initController(url, self.config[name])
        return []

    def updateControllerLatencies(self, background=None):
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

    def getControllerLatencies(self):
        latency = {}
        for url in self.latencies:
            for controller in self.urls[url]:
                latency[controller] = self.latencies[url]
        return latency

    def getBackgroundData(self):
        data = self.background_data
        self.background_data = {}
        return data

    def getControllerVersionInfo(self):
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

    def getControllerSizes(self):
        result = {}
        for c in self.config:
            result[c] = self.config[c]["init"]["num_leds"]
        return result

    def getControllerInitialized(self):
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

    def send(self, commands):
        queue = {}
        fails = []
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

    def getConfig(self):
        return self.config

    def _brightness(self):
        time.sleep(BRIGHTNESS_BUFFER_TIMER)
        while len(self.brightness_queue) > 0:
            name = list(self.brightness_queue.keys())[0]
            self._send([], self.brightness_queue[name])
            self.brightness_queue.pop(name)
        self.brightness_timer_active = False

    def getLastBrightness(self):
        return self.last_brightness

    def brightness(self, requests):
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

    def getPixels(self):
        result = {}
        for i in self.controllers:
            pixels = self.controllers[i].getPixels()
            for j in range(min(len(self.urls[i]), len(pixels))):
                result[self.urls[i][j]] = pixels[j]
        return result
