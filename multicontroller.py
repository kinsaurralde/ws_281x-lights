import threading
import requests
import time

from controller import Controller


class MultiController():
    def __init__(self, config_data):
        self.controllers = []
        self.queues = []
        self.cur_controller_id = [0]
        self.start_time = 0
        self.start_delay = .1
        if "controllers" not in config_data:
            raise KeyError
        for controller in config_data["controllers"]:
            self._add_controller(controller)

    def _add_controller(self, data):
        cur_id = len(self.controllers)
        if data["primary"] == True:
            self.controllers.append(Controller(cur_id))
            self.controllers[cur_id].init_neopixels(data)
            self.controllers[cur_id].run(0, "wipe", (255, 0, 0, 1, 250, True))
            self.controllers[cur_id].run(0, "wipe", (0, 255, 0, 1, 250, True))
            self.controllers[cur_id].run(0, "wipe", (0, 0, 255, 1, 250, True))
            self.controllers[cur_id].run(0, "wipe", (0, 0, 0, 1, 250, True))
        else:
            self.controllers.append(RemoteController(cur_id, data))
        self.queues.append([])

    def _get_all_ids(self):
        out = []
        for i in range(len(self.controllers)):
            out.append(i)
        return out

    def _set_cur_ids(self, new_ids):
        if new_ids == None:
            return
        if isinstance(new_ids, list):
            self.cur_controller_id = new_ids
        else:
            self.cur_controller_id = [new_ids]
        self.cur_controller_id = [int(i) for i in self.cur_controller_id]
        if -1 in self.cur_controller_id:
            self.cur_controller_id = self._get_all_ids()
        self.start_time = time.time()
        if len(self.cur_controller_id) > 1:
            self.start_time += self.start_delay

    def _starttime(self):
        return {
                "type": "command",
                "function": "starttime",
                "arguments":  {
                    "amount": self.start_time
                }
            }

    def _create(self, type, strip_id, function, arguments=None, stop=False):
        data = [
            {
                "type": type,
                "function": function,
                "strip_id": strip_id,
                "arguments": arguments
            }
        ]
        if stop:
            data = [{
                "type": "command",
                "function": "stopanimation",
                "strip_id": strip_id
            }] + data
        data = [self._starttime()] + data
        return data

    def _response(self):
        return {
            "error": "false",
            "message": "Threads started"
        }

    def json(self, data):
        self._set_cur_ids("-1")
        for line in data:
            if "controller_id" in line:
                self._set_cur_ids(line["controller_id"])
            for i in self.cur_controller_id:
                self.queues[i].append(line)
        for i in range(len(self.controllers)):
            threading_thread = threading.Thread(
                target=self.controllers[i].execute_json, args=[self.queues[i]])
            threading_thread.start()
            self.queues[i] = []
        return True

    def off(self, controller_id=None, strip_id=None):
        self._set_cur_ids(controller_id)
        json = self._create("command", strip_id, "off")
        for i in self.cur_controller_id:
            execute = self.controllers[i].execute_json
            thread = threading.Thread(target=execute, args=[json])
            thread.start()
        return self._response()

    def stop(self, controller_id=None, strip_id=None):
        self._set_cur_ids(controller_id)
        json = self._create("command", strip_id, "stopanimation")
        for i in self.cur_controller_id:
            execute = self.controllers[i].execute_json
            thread = threading.Thread(target=execute, args=[json])
            thread.start()
        return self._response()

    def run(self, controller_id, strip_id, function, args):
        self._set_cur_ids(controller_id)
        json = self._create("run", strip_id, function, args, True)
        for i in self.cur_controller_id:
            execute = self.controllers[i].execute_json
            thread = threading.Thread(target=execute, args=[json])
            thread.start()
        return self._response()

    def thread(self, controller_id, strip_id, function, args):
        self._set_cur_ids(controller_id)
        json = self._create("thread", strip_id, function, args)
        for i in self.cur_controller_id:
            execute = self.controllers[i].execute_json
            thread = threading.Thread(target=execute, args=[json])
            thread.start()
        return self._response()

    def animate(self, controller_id, strip_id, function, args, delay=0):
        self._set_cur_ids(controller_id)
        json = self._create("animate", strip_id, function, args, True)
        json[2]["delay_between"] = delay
        for i in self.cur_controller_id:
            execute = self.controllers[i].execute_json
            thread = threading.Thread(target=execute, args=[json])
            thread.start()
        return self._response()

    def change_settings(self, controller_id, new_settings):
        response = []
        self._set_cur_ids(controller_id)
        for i in self.cur_controller_id:
            if "break_animation" in new_settings:
                self.controllers[i].set_break_animation(
                    new_settings["break_animation"])
            if "brightness" in new_settings:
                self.controllers[i].set_brightness(new_settings["brightness"])
        return response

    def info(self):
        response = []
        for i in range(len(self.controllers)):
            response.append(self.controllers[i].info())
        return response

    def ping(self):
        data = []
        for i in self.controllers:
            start_time = time.time()
            data.append((i.ping() - start_time) * 1000)
        return data


class RemoteController():
    def __init__(self, controller_id, data):
        self.id = controller_id
        self.start_time = 0
        self.is_remote = True
        self.remote = "http://" + data["remote"]

    def _create_json(self, type, strip_id, function, arguments=None):
        return [{
            "type": type,
            "function": function,
            "strip_id": strip_id,
            "controller_id": 0,
            "arguments": arguments
        }]

    def execute_json(self, data):
        requests.post(self.remote + "/json", json=data)

    def ping(self):
        return requests.get(self.remote + "/ping").json()

    def info(self):
        r = requests.get(self.remote + "/info/get")
        data = r.json()
        data["controller_id"] = self.id
        return data

    def delay_start_time(self, value):
        self.start_time = value

    def set_brightness(self, value):
        self.execute_json(self._create_json(
            "setting", None, "brightness", value))
