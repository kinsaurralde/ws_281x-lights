#!/usr/bin/env python3
import json
import sys
import time
import argparse

from flask import Flask, render_template, json, request
from flask_socketio import SocketIO
from info import Info
from key import Keys
# from multicontroller import MultiController
from py.multicontroller import MultiController
from saves import Saves

try:
    import yaml # 3.6
except:
    import ruamel.yaml as yaml  # 3.7

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins = '*')
debug_exceptions = False  # if true, exception will be sent to web

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Debug mode', default=False)
parser.add_argument('-t', '--test', action='store_true', help='Testing mode (for non pi devices)', default=False)
parser.add_argument('-c', '--config', type=str, help='Path to config directory', default="configs/sample/")
parser.add_argument('-p', '--port', type=int, help='Port to run server on (overrides config file)', default=None)
args = parser.parse_args()

def open_yaml(path):
    data = {}
    with open(path) as open_file:
        data = yaml.load(open_file)
    return data

def create_response(data):
    response = app.response_class(response=json.dumps(
        data), status=200, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def error_response(message):
    data = {
        "error": True,
        "message": message,
    }
    return create_response(data)


def exception_handler(ex):
    if debug_exceptions:
        raise ex
    try:
        raise ex
    except ValueError as e:
        return error_response("Value Error: invalid parameter"+str(e))
    except NameError as e:
        return page_not_found("Invalid animate function: "+str(e))
    except TypeError as e:
        return error_response("Type Error: "+str(e))
    except AssertionError:
        return error_response("Assertion Error: invalid key")
    except FileNotFoundError:
        return error_response("Invalid File name or path" + str(e))


def split_key_ids(items):
    split = items.split(':')
    data = {
        "key": 0,
        "controller_ids": 0,
        "strip_id": 0
    }
    if len(split) > 0:
        if split[0] != "":
            data["key"] = int(split[0])
    if len(split) > 1:
        if split[1] != "":
            data["controller_ids"] = split[1].split(',')
    if len(split) > 2:
        if split[2] != "":
            data["strip_id"] = split[2]
    return data


def make_list(arg):
    arg = str(arg)
    if ';' in arg:
        arg = [[int(y) for y in x.split('.')] for x in arg.split(';')]
    elif '!' in arg:
        arg = float(arg[1:])
    elif '.' in arg:
        arg = [[int(x) for x in arg.split('.')]]
    elif arg in ["false", "False"]:
        arg = False
    elif arg in ["true", "True"]:
        arg = True
    return arg


@app.errorhandler(404)
def page_not_found(e):
    return error_response(str(e)), 404


@app.route('/')
def index():
    """Main control page"""
    return render_template('new_index.html', quick_actions=quick_actions)


@app.route('/info/<function>')
def info(function):
    if function == "web":
        return render_template('info.html')
    elif function == "new_web":
        return render_template('new_info.html')
    elif function == "get":
        data = mc.info()
        return create_response(data)
    else:
        return page_not_found("Info function not found")

@app.route('/ping')
def ping():
    data = mc.ping()
    print("Ping Data:", data)
    return create_response(data)

@app.route('/test/<function>')
def test(function):
    if function == "1":
        actions = [{
            "type": "run",
            "function": "chase",
            "arguments": {"r": 255, "g": 200, "b": 50},
            "framerate": 20
        }]
    elif function == "2":
        actions = [{
            "type": "run",
            "function": "chase",
            "arguments": {"r": 255, "g": 255, "b": 25, "direction": -1},
            "framerate": 2
        }]
    elif function == "3":
        actions = [{
            "type": "base",
            "function": "color",
            "arguments": {"r": 0, "g": 0, "b": 255},
            "framerate": 0
        }]
    mc.execute(actions)
    return create_response(None)

@app.route('/action', methods=['POST'])
def action():
    mc.execute(request.get_json())
    return create_response(None)

@app.route('/quickaction', methods=['POST'])
def quickaction():
    recieved = request.get_json(force=True)
    print("Quick actions recieved", recieved)
    if recieved["name"] in quick_actions["actions"]:
        mc.execute(quick_actions["actions"][recieved["name"]]["actions"], recieved["options"])
    return create_response({"recieved": recieved})

@socketio.on('connect')
def connect():
    print("Client Connected:", request.remote_addr)
    # socketio.emit('controller_urls', mc.get_urls(), room=request.sid)
    socketio.emit('connection_response', room=request.sid)

@socketio.on('disconnect')
def disconnect():
    print('Client Disconnected')

@socketio.on('get_id')
def get_id():
    mc.emit_id()

@socketio.on('ping1')
def socket_ping():
    return None
    return info.ping(request)

@socketio.on('info')
def socket_info():
    info.emit(request)

@socketio.on('test2')
def testtest():
    print("Test")
    socketio.emit('test')

@socketio.on('info_wait')
def socket_info_wait(data):
    info.set_wait(data)

controller_config = open_yaml(args.config + "controllers.yaml")
web_config = open_yaml(args.config + "web.yaml")
quick_actions = open_yaml(args.config + "quick_actions.yaml")

mc = MultiController(testing=args.test, config=controller_config["config"])
info = Info(socketio, mc)

port = 200
if "port" in web_config["config"]:
    port = int(web_config["config"]["port"])
if args.port is not None:
    port = args.port

if __name__ == '__main__':
    socketio.run(app, debug = args.debug, host = '0.0.0.0', port = port) 
