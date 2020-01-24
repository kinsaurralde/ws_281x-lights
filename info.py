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
        self.wait = 0.10
        end_time = time.time() + self.wait * count
        while this_id == self.info_id and count > 0:
            t = time.time()
            count -= 1
            if count == 50:
                self.sio.emit('info_renew', room=request.sid)
            elif count == 0:
                self.sio.emit('info_renew')
                return
            if time.time() > end_time - count * self.wait:
                continue
            a = time.time()
            pixel_info = self.c.pixel_info()
            # print("A:\t",(time.time() - a) * 1000)
            b = time.time()
            if self.remote:
                pixel_info = [pixel_info]
            # print("B:\t",(time.time() - b) * 1000)
            c = time.time()
            for i in pixel_info:
                # d = time.time()
                self.sio.emit('info_response', i)
                # print("D:\t",(time.time() - d) * 1000)
            # print("C:\t",(time.time() - c) * 1000)
            # print("T:\t\t\t\t",(time.time() - t) * 1000, "\n")
            # self.sio.sleep(self.wait * 0.9)
            #z = time.time()
            while time.time() < end_time - count * self.wait:
                self.sio.sleep(.001)
            # print("Z:\t",(time.time() - z) * 1000)

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