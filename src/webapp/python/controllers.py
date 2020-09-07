import json
import requests


class Controllers:
    def __init__(self, config, nosend):
        self.nosend = nosend
        self.config = self._setupConfig(config["controllers"])

    def _setupConfig(self, controllers):
        id_counter = 0
        configs = {}
        for controller in controllers:
            url = controller["url"]
            self._send(
                url + "/init",
                {"id": controller["strip_id"], "init": controller["init"]},
            )
            controller["id"] = id_counter
            configs[controller["name"]] = controller
        return configs

    def _send(self, url, payload, controller_id=None):
        if self.nosend:
            print(f"Would have sent to {url}:\n{payload}")
            return {"url": url, "id": controller_id, "message": "No send is true"}
        try:
            requests.post(url, data=json.dumps(payload), timeout=0.5)
        except requests.RequestException:
            print(f"Failed to send to {url}")
            return {"url": url, "id": controller_id, "message": "Connection Error"}
        return None

    def setNoSend(self, value):
        self.nosend = value

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
                        "message": "controller not found",
                    }
                )
                continue
            command["id"] = self.config[controller_name]["strip_id"]
            url = self.config[controller_name]["url"]
            if url not in queue:
                queue[url] = []
            queue[url].append(command)
        for url in queue:
            response = self._send(url + "/data", queue[url], queue[url][0]["id"])
            if response is not None:
                fails.append(response)
        return fails

    def getConfig(self):
        return self.config
