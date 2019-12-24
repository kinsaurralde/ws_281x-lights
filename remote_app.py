#!/usr/bin/env python3
import json as js
import sys
import time

from flask import Flask, json, request, render_template_string
from flask_socketio import SocketIO
from key import Keys
from controller import Controller

app = Flask(__name__)
socketio = SocketIO(app)

debug_exceptions = False  # if true, exception will be sent to web

VERBOSE = False

def create_response(data):
    response = app.response_class(response=js.dumps(
        data), status=200, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def error_response(message):
    data = {
        "error": True,
        "message": message,
    }
    return create_response(data)


@app.errorhandler(404)
def page_not_found(e):
    return error_response(str(e)), 404


@app.route('/')
def index():
    return render_template_string('<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js" integrity="sha256-bQmrZe4yPnQrLTY+1gYylfNMBuGfnT/HKsCGX+9Xuqo=" crossorigin="anonymous"></script>')

@app.route('/info/get')
def info_get():
    data = controller.info()
    return create_response(data)

@app.route('/info/active')
def info_active():
    return create_response(current_json)

@app.route('/off')
def off():
    data = controller.off()
    return create_response(data)

controller = Controller(0)

config_name = "config.json"
if len(sys.argv) > 1:   # argv[0] is this file name so one argument is length of 2
    config_name = sys.argv[1]
try:
    config_file = open(config_name, "r")
except FileNotFoundError:
    print("Config file not found")
    exit(1)
config_data = json.load(config_file)

controller.init_neopixels(config_data["controllers"][0])

keys = Keys(config_data)

controller.run(0, "wipe", (255, 0, 0, 1, 250, True), time.time())
controller.run(0, "wipe", (0, 255, 0, 1, 250, True), time.time())
controller.run(0, "wipe", (0, 0, 255, 1, 250, True), time.time())
controller.run(0, "wipe", (0, 0, 0, 1, 250, True), time.time())

needs_default = True

current_json = {}

port = 200
if "port" in config_data["info"]:
    port = int(config_data["info"]["port"])

@socketio.on('test')
def test():
    print("Testing")
    

@socketio.on('ping')
def ping(methods=['GET']):
    print("Current time is:", time.time())
    socketio.emit('ping_response', time.time())

@socketio.on('json')
def json(data, methods=['POST']):
    global current_json
    if VERBOSE:
        print("Recieved JSON:", data)
    current_json = data
    controller.execute_json(data)

@socketio.on('info')
def info(methods=['GET']):
    print("Info Requested")
    data = controller.info()
    socketio.emit('info_response', data)

@socketio.on('connect')
def test_connect():
    global needs_default
    print("Connected")
    socketio.emit('connected', {'needs_default': needs_default})
    needs_default = False

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
