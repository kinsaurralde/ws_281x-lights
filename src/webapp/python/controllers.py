import json
import time
import requests


class Controllers:
    def __init__(self, config, nosend):
        self.nosend = nosend
        self.send_counter = 0
        self.urls = {}
        self.config = self._setupConfig(config["controllers"])
        self.getControllerLatencies()

    def _setupConfig(self, controllers):
        id_counter = 0
        configs = {}
        for controller in controllers:
            url = controller["url"]
            if url not in self.urls:
                self.urls[url] = 0
            self._send(
                url + "/init",
                {"id": controller["strip_id"], "init": controller["init"]},
            )
            controller["id"] = id_counter
            configs[controller["name"]] = controller
        return configs

    def _send(self, url, payload=None, controller_id=None):
        self.send_counter += 1
        if self.nosend:
            print(f"Would have sent to {url}:\n{payload}")
            return {"url": url, "id": controller_id, "message": "No send is true"}
        try:
            if payload is None:
                requests.get(url)
            else:
                requests.post(url, data=json.dumps(payload), timeout=0.5)
        except requests.RequestException:
            print(f"Failed to send to {url}")
            return {"url": url, "id": controller_id, "message": "Connection Error"}
        return None

    def getControllerLatencies(self):
        for url in self.urls:
            start_time = time.time()
            self._send(url)
            end_time = time.time()
            latency = int((end_time - start_time) * 1000)
            previous = self.urls[url]
            if previous == 0:
                previous = latency
            self.urls[url] = (previous + latency) / 2
        print(self.urls)

    def setNoSend(self, value):
        self.nosend = value

    def send(self, commands):
        queue = {}
        fails = []
        total_estimated_latency = 0
        for command in commands:
            controller_name = command["id"]
            if controller_name not in self.config:
                fails.append(
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
        for url in queue:
            total_estimated_latency -= self.urls[url]
            print(f"Delay for {url} is {total_estimated_latency}")
            for command in queue[url]:
                command["delay"] = total_estimated_latency
            response = self._send(url + "/data", queue[url], queue[url][0]["id"])
            if response is not None:
                fails.append(response)
        if self.send_counter % 50 == 0:
            self.getControllerLatencies()
        return fails

    def getConfig(self):
        return self.config
