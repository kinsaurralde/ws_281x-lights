import socketio

from py.neopixels import NeoPixels

neo = NeoPixels(60, 255, 18, 18, 18, False, False, True)


def received_info(data):
    print("Recieved:", data[0]["pixels"])
    neo.update_pixels(data[0]['pixels'])
    neo.show()


sio = socketio.Client()
sio.connect("http://192.168.29.60:5000")

sio.on('info_response', received_info)




