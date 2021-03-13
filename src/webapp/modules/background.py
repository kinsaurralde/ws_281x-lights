import threading
import time


class Background:
    """Runs thread in background to provide webapps with updates / pixel status"""

    def __init__(self, socketio, controller):
        self.socketio = socketio
        self.controller = controller
        self.active = True
        self.delay_ms = 100
        # self.pixel_interval = 50
        self.emit_delay_ms = 1000
        self.full_cycle = 10
        self.data = {}
        self.start_time = time.time()

    def startLoop(self):
        """Start background loop"""
        thread = threading.Thread(target=self._loop)
        thread.start()

    def updatePing(self):
        """Update controller ping"""
        self.controller.updateControllerLatencies(self)
        self.data["ping"] = self.controller.getControllerLatencies()

    def updateData(self):
        """Update background data"""
        self.data.update(self.controller.getBackgroundData())

    def emitUpdate(self):
        """Emit update"""
        if len(self.data) > 0:
            self.socketio.emit("update", self.data)

    def _loop(self):
        counter = 0
        loop_counter = 0
        self.data = {}
        while self.active:
            if counter % self.emit_delay_ms == 0:
                if loop_counter % self.full_cycle == 0:
                    self.updatePing()
                loop_counter += 1
                counter = 0
                self.emitUpdate()
                self.data = {}
            time.sleep(self.delay_ms / 1000)
            counter += self.delay_ms
