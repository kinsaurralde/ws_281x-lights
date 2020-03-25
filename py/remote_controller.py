import time
import socketio

from py.controller import Controller


class RemoteController(Controller):
    def __init__(self, name_id, config, testing=False):
        self.name_id = name_id
        self.config = config
        self.sio = socketio.Client()
        self.sio.on('connection_response', self._connect_response)
        self.sio.on('disconnect_response', self._disconnect_response)
        self.sio.on('ping_response', self._ping_response)
        self.connected = False
        self.url = "http://" + config["url"]
        self._connect(True)
        self.ping_wait = False
        self.ping_mid = 0
        super().__init__(name_id, config, testing) 

    def _connect(self, setup=False):
        try:
            self.sio.connect(self.url)
            if setup:
                self._emit('setup_controller', {"name_id": self.name_id, "config": self.config})
        except socketio.exceptions.ConnectionError:
            print("Failed to connect to", self.url)

    def _connect_response(self, tmp):
        print("Connected to", self.url)
        self.connected = True

    def _disconnect_response(self):
        print("Disconnected from", self.url)
        self.connected = False

    def _ping_response(self, data):
        self.ping_wait = False
        self.ping_mid = data["mid_time"]

    def _emit_response(self, start_time):
        print("Emit Calledback", (time.time() - start_time) * 1000)

    def _emit(self, message, data):
        if self.connected:
            emit_data = {"data": data, "info": {}}
            emit_data["info"]["version"] = "test"
            start_time = time.time()
            self.sio.emit(message, emit_data, self._emit_response(start_time))
        else:
            self._connect()

    def ping(self):
        self.ping_wait = True
        self._emit('ping', {})
        pingtimeout = time.time() + 1
        while self.ping_wait:
            time.sleep(0.001)
            if time.time() > pingtimeout:
                self.connected = False
                print("Ping to", self.url, "timed out")
                return 0
        return self.ping_mid

    def set_strip(self, data):
        self._emit('set_strip', {"data": data})
        super().set_strip(data)
        
    def set_framerate(self, value, vs_id):
        self._emit('set_framerate', {"value": value, "vs_id": vs_id})
        super().set_framerate(value, vs_id)

    def set_settings(self, settings):
        self._emit('set_settings', {"settings": settings})
        super().set_settings(settings)
        
    def set_base(self, data, vs_id):
        self._emit('set_base', {"data": data, "vs_id": vs_id})
        super().set_base(data, vs_id)
        
    def set_animation(self, data, vs_id):
        self._emit('set_animation', {"data": data, "vs_id": vs_id})
        super().set_animation(data, vs_id)
        
    def set_control(self, data, vs_id):
        self._emit('set_control', {"data": data, "vs_id": vs_id})
        super().set_control(data, vs_id)

    def set_brightness(self, data):
        self._emit('set_brightness', {"data": data})
        super().set_brightness(data)
