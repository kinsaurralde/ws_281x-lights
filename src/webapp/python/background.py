import threading
import time


class Background:
    def __init__(self, socketio, controller):
        self.socketio = socketio
        self.controller = controller
        self.active = True
        self.delay_ms = 50
        self.full_loop_ms = 1000
        self.update_after_loops = 8
        self.start_time = time.time()

    def startLoop(self):
        thread = threading.Thread(target=self._loop)
        thread.start()

    def _loop(self):
        counter = 0
        loop_counter = 0
        data = {}
        while self.active:
            if loop_counter % self.update_after_loops == 0:
                thread = threading.Thread(
                    target=self.controller.updateControllerLatencies
                )
                thread.start()
                loop_counter = 1
            if loop_counter % self.update_after_loops == self.update_after_loops // 2:
                data.update(self.controller.getBackgroundData())
                if counter % self.full_loop_ms == 0:
                    data["ping"] = self.controller.getControllerLatencies()
            if counter % self.full_loop_ms == 0:
                loop_counter += 1
                counter = 0
                if len(data) > 0:
                    self.socketio.emit("update", data)
                data = {}
            time.sleep(self.delay_ms / 1000)
            counter += self.delay_ms
