#!/usr/bin/env python3

import json
import sys
import time

from flask import Flask, render_template, json, request
from key import Keys
from controller import Controller
from multicontroller import MultiController
from saves import Saves

app = Flask(__name__)
debug_exceptions = False  # if true, exception will be sent to web


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
    return render_template('index.html')


@app.route('/info/<function>')
def info(function):
    if function == "web":
        return render_template('info.html')
    elif function == "get":
        data = mc.info()
        return create_response(data)
    else:
        return page_not_found("Info function not found")


@app.route('/<key>/<strip_id>/key/<function>')
@app.route('/<key>/<strip_id>/key/<function>/<param>')
def key(strip_id, key, function, param=None):
    try:
        params = []
        if param != None:
            params = param.split(',')
        keys.check_key(key, -1)
        if function == "web":
            return render_template('keys.html')
        keys.run_function(function, params)
        return create_response(keys.get_keys(key))
    except Exception as e:
        return exception_handler(e)


@app.route('/<key_ids>/off')
def off(key_ids):
    try:
        data = split_key_ids(key_ids)
        keys.check_key(data["key"], data["strip_id"])
        controller_response = mc.off(
            data["controller_ids"], int(data["strip_id"]))
    except Exception as e:
        return exception_handler(e)
    return create_response(controller_response)


@app.route('/<key_ids>/stopanimation')
def stopanimation(key_ids):
    data = split_key_ids(key_ids)
    controller_response = mc.stop(
        data["controller_ids"], int(data["strip_id"]))
    return create_response(controller_response)


@app.route('/settings/<controller_ids>/<args>')
def change_settings(controller_ids, args):
    settings = args.split(",")
    new_settings = {}
    for setting in settings:
        current = setting.split("=")
        if current[0] == "break":
            if current[1] == "true":
                new_settings["break_animation"] = True
            else:
                new_settings["break_animation"] = False
        if current[0] == "brightness":
            new_settings["brightness"] = int(current[1])
    mc.change_settings(controller_ids.split(','), new_settings)
    return create_response({})


@app.route('/<key_ids>/run/<function>')
@app.route('/<key_ids>/run/<function>/<args>')
def run(key_ids, function, args=None):
    try:
        data = split_key_ids(key_ids)
        keys.check_keys(data["key"], data["controller_ids"])
        if args is not None:
            args = [int(x) if x.lstrip('-').isdigit() else make_list(x) for x in args.split(',')]
        controller_response = mc.run(data["controller_ids"], int(
            data["strip_id"]), function, args)
        return create_response(controller_response)
    except Exception as e:
        return exception_handler(e)


@app.route('/<key_ids>/thread/<function>/<args>')
def thread(key_ids, function, args):
    try:
        data = split_key_ids(key_ids)
        keys.check_key(data["key"], data["strip_id"])
        args = [int(x) if x.lstrip('-').isdigit() else make_list(x) for x in args.split(',')]
        controller_response = mc.thread(
            data["controller_ids"], int(data["strip_id"]), function, args)
        return create_response(controller_response)
    except Exception as e:
        return exception_handler(e)


@app.route('/<key_ids>/animate/<function>/<args>')
@app.route('/<key_ids>/animate/<function>/<args>/<delay>')
def animate(key_ids, function, args, delay=0):
    try:
        data = split_key_ids(key_ids)
        keys.check_key(data["key"], data["strip_id"])
        args = [int(x) if x.lstrip('-').isdigit() else make_list(x) for x in args.split(',')]
        controller_response = mc.animate(data["controller_ids"],
                                         int(data["strip_id"]), function, args, delay)
        return create_response(controller_response)
    except Exception as e:
        return exception_handler(e)


@app.route('/json', methods=['GET', 'POST'])
def post_json():
    data = request.get_json()
    return create_response(mc.json(data))

@app.route('/saved/<folder>/<function>')
@app.route('/saved/<folder>/<function>/<path>')
@app.route('/saved/<folder>/<function>/<path>/<data>', methods=['GET', 'POST'])
def saved(folder, function, path = None, data = None):
    try:
        return_data = {}
        data = saves.run_function(function, folder, path, data)
        if function == "run":
            return create_response(mc.json(data))
        return create_response(data)
    except Exception as e:
        return exception_handler(e)


@app.route('/ping')
def ping():
    data = mc.ping()
    print("Ping Data:", data)
    return create_response(data)


config_name = "sample_config.json"
if len(sys.argv) > 1:
    config_name = sys.argv[1]
debug_mode = False
if len(sys.argv) > 2:
    debug_mode = bool(sys.argv[2])
try:
    config_file = open(config_name, "r")
except FileNotFoundError:
    print("Config file not found")
    exit(1)
config_data = json.load(config_file)
print("Config data read from", config_name, ":\n", config_data)

mc = MultiController(config_data)

keys = Keys(config_data)

saves = Saves()

port = 200
if "port" in config_data["info"]:
    port = int(config_data["info"]["port"])

if __name__ == '__main__':
    app.run(debug = debug_mode, host = '0.0.0.0', port = port, threaded = True) 
