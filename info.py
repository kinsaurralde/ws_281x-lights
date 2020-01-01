import time

class Info:
    def __init__(self, sio, controller, is_remote=False):
        self.sio = sio
        self.c = controller
        self.info_id = 0
        self.remote = is_remote
        self.wait = 0.015

    def emit(self, request):
        self.info_id += 1
        this_id = self.info_id
        count = 1000
        self.wait = 0.015
        end_time = time.time() + self.wait * count
        while this_id == self.info_id and count > 0:
            count -= 1
            if time.time() > end_time - count * self.wait:
                continue 
            pixel_info = self.c.pixel_info()
            if self.remote:
                pixel_info = [pixel_info]
            for i in pixel_info:
                self.sio.emit('info_response', i)
            self.sio.sleep(self.wait)
            if count == 50:
                self.sio.emit('info_renew', room=request.sid)
            elif count == 0:
                self.sio.emit('info_renew')

    def set_wait(self, value):
        self.wait = value