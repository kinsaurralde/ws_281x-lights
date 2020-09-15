import json
import time
import threading
import requests

BRIGHTNESS_BUFFER_TIMER = 0.01


class Controllers:
    def __init__(self, config, nosend, version_info):
        self.version_info = version_info
        self.nosend = nosend
        self.send_counter = 0
        self.urls = {}
        self.brightness_queue = {}
        self.brightness_timer_active = False
        self.fails = []
        self.config = self._setupConfig(config["controllers"])
        self.getControllerLatencies()

    def _setupConfig(self, controllers):
        id_counter = 0
        configs = {}
        threads = []
        for controller in controllers:
            url = controller["url"]
            if url not in self.urls:
                self.urls[url] = 0
            threads.append(
                self._send(
                    url + "/init",
                    {"id": controller["strip_id"], "init": controller["init"]},
                )
            )
            controller["id"] = id_counter
            configs[controller["name"]] = controller
        for thread in threads:
            thread.join()
        return configs

    def _send(self, url, payload=None, controller_id=None):
        thread = threading.Thread(
            target=self._sending_thread, args=(url, payload, controller_id)
        )
        thread.start()
        return thread

    def _sending_thread(self, url, payload=None, controller_id=None):
        self.send_counter += 1
        if self.nosend:
            print(f"Would have sent to {url}:\n{payload}")
            self.fails.append(
                {"url": url, "id": controller_id, "message": "No send is true"}
            )
        try:
            if payload is None:
                return requests.get(url)
            return requests.post(url, data=json.dumps(payload), timeout=0.5)
        except requests.RequestException:
            print(f"Failed to send to {url}")
            self.fails.append(
                {"url": url, "id": controller_id, "message": "Connection Error"}
            )
        return []

    def getControllerLatencies(self):
        for url in self.urls:
            start_time = time.time()
            self._sending_thread(url)
            end_time = time.time()
            latency = int((end_time - start_time) * 1000)
            previous = self.urls[url]
            if previous == 0:
                previous = latency
            self.urls[url] = (previous + latency) / 2
        print("Controller Latencies", self.urls)

    def getControllerVersionInfo(self):
        self.fails = []
        data = []
        version_match = True
        hash_match = True
        for url in self.urls:
            response = self._sending_thread(url + "/versioninfo").json()
            data.append(response)
            if (
                response["major"] != self.version_info["major"]
                or response["minor"] != self.version_info["minor"]
                or response["patch"] != self.version_info["patch"]
            ):
                version_match = False
                self.fails.append(
                    {"url": url, "id": "version", "message": "Version doesnt match"}
                )
            if (
                response["esp_hash"] != self.version_info["esp_hash"]
                or response["rpi_hash"] != self.version_info["rpi_hash"]
            ):
                hash_match = False
                self.fails.append(
                    {"url": url, "id": "hash", "message": "Hash doesnt match"}
                )
        return {
            "versioninfo": data,
            "fails": self.fails,
            "webapp": self.version_info,
            "version_match": version_match,
            "hash_match": hash_match,
        }

    def getControllerInitialized(self):
        self.fails = []
        data = {}
        for url in self.urls:
            response = self._sending_thread(url + "/init").json()
            for controller in self.config:
                if self.config[controller]["url"] == url:
                    response_index = int(self.config[controller]["strip_id"])
                    if response_index < 0 or response_index >= len(response):
                        self.fails.append(
                            {
                                "url": url,
                                "id": response_index,
                                "message": "Strip id does not exist on remote controller",
                            }
                        )
                    else:
                        data[controller] = response[response_index]
        return {"fails": self.fails, "initialized": data}

    def setNoSend(self, value):
        self.nosend = value

    def send(self, commands):
        queue = {}
        self.fails = []
        total_estimated_latency = 0
        for command in commands:
            controller_name = command["id"]
            if controller_name not in self.config:
                self.fails.append(
                    {
                        "url": "localhost",
                        "id": controller_name,
                        "message": "controller not found",
                    }
                )
                continue
            command["id"] = self.config[controller_name]["strip_id"]
            url = self.config[controller_name]["url"]
            if url not in queue:
                total_estimated_latency += self.urls[url]
                queue[url] = []
            queue[url].append(command)
        threads = []
        for url in queue:
            total_estimated_latency -= self.urls[url]
            for command in queue[url]:
                command["delay"] = total_estimated_latency
            threads.append(self._send(url + "/data", queue[url], queue[url][0]["id"]))
        for thread in threads:
            thread.join()
        if self.send_counter % 25 == 0:
            self.getControllerLatencies()
        return self.fails

    def getConfig(self):
        return self.config

    def _brightness(self):
        time.sleep(BRIGHTNESS_BUFFER_TIMER)
        while len(self.brightness_queue) > 0:
            name = list(self.brightness_queue.keys())[0]
            self._send(self.brightness_queue[name])
            self.brightness_queue.pop(name)
        self.brightness_timer_active = False

    def brightness(self, requests):
        for request in requests:
            name = request["name"]
            value = request["value"]
            url = self.config[name]["url"]
            self.brightness_queue[name] = (
                url + f"/brightness?value={value}&id={self.config[name]['strip_id']}"
            )
            if not self.brightness_timer_active:
                self.brightness_timer_active = True
                thread = threading.Thread(target=self._brightness())
                thread.start()
