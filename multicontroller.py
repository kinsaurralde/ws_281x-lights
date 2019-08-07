import threading
import requests

from controller import Controller


class MultiController():
    def __init__(self, config_data):
        self.controllers = []
        self.queues = []
        self.cur_controller_id = [0]
        if "controllers" not in config_data:
            raise KeyError
        for controller in config_data["controllers"]:
            self._add_controller(controller)

    def _add_controller(self, data):
        cur_id = len(self.controllers)
        if data["primary"] == True:
            self.controllers.append(Controller(cur_id))
            self.controllers[cur_id].init_neopixels(data)
            self.controllers[cur_id].run(0, "wipe", (255, 0, 0, 1, 1))
            self.controllers[cur_id].run(0, "wipe", (0, 255, 0, 1, 1))
            self.controllers[cur_id].run(0, "wipe", (0, 0, 255, 1, 1))
            self.controllers[cur_id].run(0, "wipe", (0, 0, 0, 1, 1))
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

    def json(self, data):
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
        response = []
        self._set_cur_ids(controller_id)
        for i in self.cur_controller_id:
            response.append(self.controllers[i].off(strip_id))
        return response

    def stop(self, controller_id=None, strip_id=None):
        response = []
        self._set_cur_ids(controller_id)
        for i in self.cur_controller_id:
            response.append(self.controllers[i].stop(strip_id))
        return response

    def run(self, controller_id, strip_id, function, args):
        response = []
        self._set_cur_ids(controller_id)
        for i in self.cur_controller_id:
            response.append(self.controllers[i].run(strip_id, function, args))
        return response

    def thread(self, controller_id, strip_id, function, args):
        response = []
        self._set_cur_ids(controller_id)
        for i in self.cur_controller_id:
            response.append(self.controllers[i].thread(
                strip_id, function, args))
        return response

    def animate(self, controller_id, strip_id, function, args, delay_between=0):
        response = []
        self._set_cur_ids(controller_id)
        for i in self.cur_controller_id:
            response.append(self.controllers[i].animate(
                strip_id, function, args, delay_between))
        return response

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


class RemoteController():
    def __init__(self, controller_id, data):
        self.id = controller_id
        self.is_remote = True
        self.remote = "http://" + data["remote"]

    def _create_json(self, type, strip_id, function, arguments=None):
        return {
           "type": type,
            "function": function,
            "strip_id": strip_id,
            "controller_id": 0,
            "arguments": arguments 
        }

    def execute_json(self, data):
        requests.post(self.remote + "/json", json=data)

    def info(self):
        r = requests.get(self.remote + "/info/get")
        data = r.json()
        data["controller_id"] = self.id
        return data

    def set_brightness(self, value):
        self.execute_json([self._create_json("setting", None, "brightness", value)])

    def off(self, strip_id=None):
        self.execute_json([self._create_json("command", strip_id, "off")])

    def stop(self, strip_id=None):
        self.execute_json([self._create_json("command", strip_id, "stopanimation")])

    def run(self, strip_id, function, arguments=None):
        self.execute_json([self._create_json("run", strip_id, function, arguments)])

    def thread(self, strip_id, function, arguments=None):
        self.execute_json([self._create_json("thread", strip_id, function, arguments)])

    def animate(self, strip_id, function, arguments=None, delay_between=0):
        data = self._create_json("animate", strip_id, function, arguments)
        data["delay_between"] = delay_between
        self.execute_json([data])
