#!/usr/bin/env python3
import time
import argparse

from flask import Flask, render_template, json, request, send_from_directory
from flask_socketio import SocketIO
from rpi_ws281x import Adafruit_NeoPixel

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins = '*')

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Debug mode', default=False)
parser.add_argument('-t', '--test', action='store_true', help='Testing mode (for non pi devices)', default=False)
parser.add_argument('-p', '--port', type=int, help='Port to run server', default=5001)
args = parser.parse_args()

def create_response(data):
    response = app.response_class(response=json.dumps(
        data), status=200, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@socketio.on('connect')
def connect():
    print("Client Connected:", request.remote_addr)
    socketio.emit('connection_response', room=request.sid)

@socketio.on('disconnect')
def disconnect():
    print('Client Disconnected')

@socketio.on('neopixel_update')
def update(data):
    reciever.update(data)

@socketio.on('neopixel_set_brightness')
def set_brightness(data):
    print("Set brightness", data["value"])
    reciever.set_brightness(data)

class Reciever:
    def __init__(self, testing=False):
        self.testing = testing
        self.neo = None
        self.ready = False
        self.setup_neopixels(None)

    def setup_neopixels(self, data):
        if self.ready:
            return
        self.led_count = 60
        self.strip = Adafruit_NeoPixel(self.led_count, 18, 800000, 10, False, 255, False)
        if not self.testing:
            self.strip.begin()
        self.ready = True

    def set_brightness(self, data):
        if not self.ready or self.testing:
            return
        self.strip.setBrightness(data["value"])

    def update(self, data):
        if not self.ready or self.testing:
            return
        for i in range(min(self.led_count, len(data["pixels"]))):
            self.strip.setPixelColor(i, data["pixels"][i])
        self.strip.show()

reciever = Reciever(testing=args.test)

if __name__ == '__main__':
    socketio.run(app, debug = args.debug, host = '0.0.0.0', port = args.port, use_reloader = False) 
