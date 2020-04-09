import time

class Info:
    def __init__(self, sio, controller, is_remote=False):
        self.sio = sio
        self.c = controller
        self.info_id = 0
        self.remote = is_remote
        self.wait = .02

    def emit(self, request):
        self.info_id += 1
        this_id = self.info_id
        count = 1000
        end_time = time.time() + self.wait * count
        while this_id == self.info_id and count > 0:
            count -= 1
            if count == 50:
                self.sio.emit('info_renew', room=request.sid)
            elif count == 0:
                self.sio.emit('info_renew')
                return
            if time.time() > end_time - count * self.wait:
                continue
            self.sio.emit('info_response', self.c.pixel_info())
            while time.time() < end_time - count * self.wait:
                self.sio.sleep(.001)
            

    def ping(self, request):
        response = []
        cur_time = time.time()
        for i in self.c.get_local_controllers():
            response.append({
                "controller_id": i,
                "time": cur_time
            })
        return response

    def set_wait(self, value):
        self.wait = value
