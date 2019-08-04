#!/usr/bin/env python3

import json
import sys

from flask import Flask, json, request
from key import Keys
from controller import Controller


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


@app.errorhandler(404)
def page_not_found(e):
    return error_response(str(e)), 404

@app.route('/info/get')
def info():
    data = controller.info()
    return create_response(data)


@app.route('/json', methods=['GET', 'POST'])
def post_json():
    data = request.get_json()
    return create_response(controller.execute_json(data))


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
print("Config data read from", config_name, ":", config_data)
controller.init_neopixels(config_data["controllers"][0])

keys = Keys(config_data)

controller.run(0, "wipe", (255, 0, 0, 1, 1))
controller.run(0, "wipe", (0, 255, 0, 1, 1))
controller.run(0, "wipe", (0, 0, 255, 1, 1))
controller.run(0, "wipe", (0, 0, 0, 1, 1))

port = 200
if "port" in config_data["info"]:
    port = int(config_data["info"]["port"])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
