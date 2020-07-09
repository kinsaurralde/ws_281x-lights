#!/usr/bin/env python3
import time
import argparse

from flask import Flask, render_template, json, request, send_from_directory
from flask_socketio import SocketIO
from py.controller import Controller

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

def check_valid(request):
    if controller is None:
        return {"valid": False}
    if request["info"]["version"] != "test":
        return {"valid": False}
    return {"valid": True, "args": request["data"]}

@app.route('/')
def index():
    """Main control page"""
    if controller is None:
        return "Controller is not setup"
    return create_response({"controller_info": controller.info(), "pixels": controller.get_pixels()})

@socketio.on('connect')
def connect():
    print("Client Connected:", request.remote_addr)
    socketio.emit('connection_response', room=request.sid)
    if controller is not None:
        controller.set_settings([{"on": True}])
        controller.set_control([-1] * controller.num_pixels())

@socketio.on('disconnect')
def disconnect():
    print("Client Disconnected:", request.remote_addr)
    socketio.emit('disconnect_response', room=request.sid)
    if controller is not None:
        controller.set_settings([{"on": False}])
        controller.set_control([0] * controller.num_pixels())

@socketio.on('setup_controller')
def setup_controller(data):
    global controller
    if controller is None:
        info = data["info"]
        data = data["data"]
        print("Setting up controller with", data)
        controller = Controller(**data, testing=args.test)

@socketio.on('set_strip')
def set_strip(data):
    r = check_valid(data)
    if r["valid"]:
        controller.set_strip(**r["args"])

@socketio.on('set_framerate')
def set_framerate(data):
    r = check_valid(data)
    if r["valid"]:
        controller.set_framerate(**r["args"])

@socketio.on('set_settings')
def set_settings(data):
    r = check_valid(data)
    if r["valid"]:
        controller.set_settings(**r["args"])

@socketio.on('set_base')
def set_base(data):
    r = check_valid(data)
    if r["valid"]:
        controller.set_base(**r["args"])
    
@socketio.on('set_animation')
def set_animation(data):
    print("Set Animation", time.time())
    r = check_valid(data)
    if r["valid"]:
        controller.set_animation(**r["args"])
    
@socketio.on('set_control')
def set_control(data):
    r = check_valid(data)
    if r["valid"]:
        controller.set_control(**r["args"])

@socketio.on('set_brightness')
def set_brightness(data):
    r = check_valid(data)
    if r["valid"]:
        controller.set_brightness(**r["args"])

@socketio.on('ping')
def ping(data):
    socketio.emit('ping_response', {"mid_time": time.time()})

connected = False
controller = None

if __name__ == '__main__':
    socketio.run(app, debug = args.debug, host = '0.0.0.0', port = args.port, use_reloader = False) 
