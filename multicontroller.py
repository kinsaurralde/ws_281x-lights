import requests
import time
import socketio

from controller import Controller


class MultiController():
    def __init__(self, config_data, default_vars, testing = False):
        self.testing = testing
        self.controllers = []
        self.queues = []
        self.history = []
        self.history_length = 5
        self.cur_controller_id = [0]
        self.start_time = 0
        self.start_delay = .05
        self.default_vars = default_vars
        if "controllers" not in config_data:
            raise KeyError
        for controller in config_data["controllers"]:
            self._add_controller(controller)
        self.json(self.default_vars)

    def _add_controller(self, data):
        cur_id = len(self.controllers)
        if data["primary"] == True:
            self.controllers.append(Controller(cur_id, self.testing))
            self.controllers[cur_id].init_neopixels(data)
            self.controllers[cur_id].run(0, "wipe", (255, 0, 0, 1, 250, True), time.time())
            self.controllers[cur_id].run(0, "wipe", (0, 255, 0, 1, 250, True), time.time())
            self.controllers[cur_id].run(0, "wipe", (0, 0, 255, 1, 250, True), time.time())
            self.controllers[cur_id].run(0, "wipe", (0, 0, 0, 1, 250, True), time.time())
            time.sleep(.1)
        else:
            self.controllers.append(RemoteController(cur_id, data, self.default_vars))
        self.queues.append([])
        self.history.append({
            "pos": -1,
            "data": [{}] * self.history_length
        })


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

    def _update_history(self, id, data):
        self.history[id]["pos"] += 1
        if self.history[id]["pos"] >= self.history_length:
            self.history[id]["pos"] = 0
        self.history[id]["data"][self.history[id]["pos"]] = data


    def get_history(self):
        return self.history

    def valid_id(self, i):
        if not isinstance(i, int):
            return False
        if i < 0 or i > len(self.controllers):
            return False
        return True

    def json(self, data, controller_id=None):
        self._set_cur_ids("-1")
        self._set_cur_ids(controller_id)
        for line in data:
            if "controller_id" in line:
                self._set_cur_ids(line["controller_id"])
            for i in self.cur_controller_id:
                self.queues[i].append(line)
        for i in range(len(self.controllers)):
            data = [self._starttime()] + self.queues[i]
            self.controllers[i].execute_json(data)
            self._update_history(i, data)
            self.queues[i] = []
        return self._response()

    def off(self, controller_id=None, strip_id=None):
        self._set_cur_ids(controller_id)
        json = self._create("command", strip_id, "off")
        for i in self.cur_controller_id:
            self.controllers[i].execute_json(json)
        return self._response()

    def stop(self, controller_id=None, strip_id=None):
        self._set_cur_ids(controller_id)
        json = self._create("command", strip_id, "stopanimation")
        for i in self.cur_controller_id:
            self.controllers[i].execute_json(json)
        return self._response()

    def run(self, controller_id, strip_id, function, args):
        self._set_cur_ids(controller_id)
        json = self._create("run", strip_id, function, args, True)
        for i in self.cur_controller_id:
            self.controllers[i].execute_json(json)
        return self._response()

    def thread(self, controller_id, strip_id, function, args):
        self._set_cur_ids(controller_id)
        json = self._create("thread", strip_id, function, args)
        for i in self.cur_controller_id:
            self.controllers[i].execute_json(json)
        return self._response()

    def animate(self, controller_id, strip_id, function, args, delay=0):
        self._set_cur_ids(controller_id)
        json = self._create("animate", strip_id, function, args, True)
        json[2]["delay_between"] = delay
        for i in self.cur_controller_id:
            self.controllers[i].execute_json(json)
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

    def controller_functions(self, function, data = None):
        if function == "status":
            result = []
            for i in range(len(self.controllers)):
                result.append([self.controllers[i].is_enabled(), self.controllers[i].is_connected()])
            return result
        elif function == "enable":
            if self.valid_id(int(data)):
                self.controllers[int(data)].toggle_enable(True)
                return self.info()
        elif function == "disable":
            if self.valid_id(int(data)):
                self.controllers[int(data)].toggle_enable(False)
                return self.info()
        return None

    def info(self):
        response = []
        ping_data = self.ping()
        controller_status = self.controller_functions("status")
        for i in range(len(self.controllers)):
            response.append(self.controllers[i].info())
            response[len(response) - 1]["ping"] = ping_data[i]
            response[len(response) - 1]["enabled"] = controller_status[i]
        return response

    def pixel_info(self):
        response = []
        for i in range(len(self.controllers)):
            info = self.controllers[i].pixel_info()
            if info is not None:
                response.append(info)
        return response

    def ping(self):
        data = []
        for i in self.controllers:
            start_time = time.time()
            ping_time = i.ping()
            if ping_time != "Error" and ping_time != "Disabled":
                data.append((ping_time - start_time) * 1000)
            else:
                data.append(-1)
        return data


class RemoteController():
    def __init__(self, controller_id, data, default_vars):
        self.default_vars = default_vars
        self.id = controller_id
        self.start_time = 0
        self.response_timeout = .250
        self.is_remote = True
        self.remote = "http://" + data["remote"]
        self.sio = socketio.Client()
        self.connected = False
        self.attempt_connect = True
        self._connect()

    def _connect(self):
        self._disconnect()
        if self.attempt_connect is False:
            print("Connection setting is off for", self.remote)
            return False
        try:
            self.sio.on('connected', self._connect_response)
            self.sio.on('ping_response', self._ping_response)
            self.sio.on('info_response', self._info_response)
            self.sio.connect(self.remote)
            self.sio.emit('ping')
            self.connected = True
            print("Connection Suceeded for", self.remote)
            return True
        except:
            print("Connection Failed for", self.remote)
            self.connected = False
            return False

    def _disconnect(self):
        try:
            self.sio.disconnect()
        except:
            print("An error occured when disconnecting", self.remote)
        self.connected = False
        print("Disconnected from", self.remote)

    def _connect_response(self, data):
        if data["needs_default"]:
            self.execute_json(self.default_vars)

    def _ping_response(self, data):
        print("ping called back", data, "from", self.remote)
        self.ping_data = data
        self.waiting_ping = False

    def _info_response(self, data):
        print("Info called back from", self.remote)
        self.info_data = data
        self.waiting_info = False

    def _emit(self, message, data = None):
        if self.attempt_connect is False:
            print("Connection setting is off for", self.remote)
            return
        if self.connected:
            self.sio.emit(message, data)
        else:
            print("Attempting to reconnect", self.remote)
            if self._connect():
                self.sio.emit(message, data)
            else:
                self.connected = False

    def _create_json(self, type, strip_id, function, arguments=None):
        return [{
            "type": type,
            "function": function,
            "strip_id": strip_id,
            "controller_id": 0,
            "arguments": arguments
        }]

    def is_enabled(self):
        return self.attempt_connect

    def is_connected(self):
        return self.connected

    def toggle_enable(self, value):
        self._disconnect()
        if value is None:
            self.attempt_connect = not self.attempt_connect
        else:
            self.attempt_connect = bool(value)
        if self.attempt_connect is True:
            self._connect()

    def execute_json(self, data):
        self._emit('json', data)

    def ping(self):
        self._emit('ping')
        self.waiting_ping = True
        send_time = time.time()
        if self.attempt_connect is False:
            return "Disabled"
        while self.waiting_ping:
            if time.time() - send_time > self.response_timeout or not self.attempt_connect:
                print(self.remote, "did not respond in time or was disabled")
                return "Error"
            time.sleep(.01)
        return self.ping_data

    def info(self):
        self._emit('info')
        self.waiting_info = True
        send_time = time.time()
        while self.waiting_info:
            if time.time() - send_time > self.response_timeout or not self.attempt_connect:
                return {
                    "error": True
                }
            time.sleep(.01)
        self.info_data["error"] = False
        return self.info_data

    def pixel_info(self):
        return None

    def delay_start_time(self, value):
        self.start_time = value

    def set_brightness(self, value):
        self.execute_json(self._create_json("setting", None, "brightness", value))
