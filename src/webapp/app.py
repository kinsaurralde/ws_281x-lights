#!/usr/bin/env python3
import json
import argparse

from collections import OrderedDict

from flask import Flask, json, render_template, request
from flask_socketio import SocketIO
from engineio.payload import Payload

import python

from version import *

try:
    import yaml  # 3.6
except:
    import ruamel.yaml as yaml  # 3.7

Payload.max_decode_packets = 50

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--debug", action="store_true", help="Debug mode", default=False
)
parser.add_argument(
    "-t", "--test", action="store_true", help="Testing mode (localtest)", default=False,
)
parser.add_argument(
    "--nosend",
    action="store_true",
    help="Dont send to controllers (For testing)",
    default=False,
)
parser.add_argument(
    "-c",
    "--config",
    type=str,
    help="Path to controller config",
    default="config/controllers_sample.yaml",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    help="Port to run server on (overrides config file)",
    default=5000,
)
parser.add_argument(
    "-b",
    "--background",
    action="store_false",
    help="Disable Background Information Thread",
    default=True,
)

args = parser.parse_args()

VERSION_INFO = {
    "major": MAJOR,
    "minor": MINOR,
    "patch": PATCH,
    "esp_hash": ESP_HASH,
    "rpi_hash": RPI_HASH,
}


def getNosend():
    return args.nosend


def open_yaml(path):
    data = {}
    with open(path) as open_file:
        data = yaml.safe_load(open_file)
    return data


def create_response(data, ordered=False):
    payload = data
    if ordered:
        payload = OrderedDict(data)
    response = app.response_class(
        response=json.dumps(payload, sort_keys=False),
        status=200,
        mimetype="application/json",
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
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


@app.route("/")
def index():
    """Main control page"""
    return render_template("index.html")


@app.route("/data", methods=["POST"])
def handleData():
    data = []
    try:
        data = json.loads(request.data)
    except ValueError:
        response = {"error": True, "message": "JSON Decode Error"}
        return create_response(response)
    controllers.setNoSend(getNosend())
    fails = controllers.send(data)
    response = {"error": len(fails) > 0, "message": fails}
    return create_response(response)


@app.route("/docs")
def docs():
    """Documentation"""
    return render_template("index.html")


@app.route("/getanimations")
def getanimations():
    return create_response(animations_config)


@app.route("/getcolors")
def getcolors():
    return create_response(colors_config)


@app.route("/getcontrollers")
def getcontrollers():
    return create_response(controllers.getConfig(), True)


@app.route("/getversioninfo")
def getversioninfo():
    return create_response(controllers.getControllerVersionInfo())


@app.route("/getinitialized")
def getinitialized():
    return create_response(controllers.getControllerInitialized())


@app.route("/enable")
def enableControllers():
    fails = controllers.enableController(request.args.get("name"))
    return create_response({"error": len(fails) > 0, "message": fails})


@app.route("/disable")
def disableControllers():
    fails = controllers.disableController(request.args.get("name"))
    return create_response({"error": len(fails) > 0, "message": fails})


@socketio.on("connect")
def connect():
    print("Client Connected:", request.remote_addr)
    socketio.emit("connection_response", room=request.sid)


@socketio.on("disconnect")
def disconnect():
    print("Client Disconnected")


@socketio.on("set_brightness")
def setBrightness(json):
    controllers.brightness(json)


animations_config = open_yaml("config/animations.yaml")
colors_config = open_yaml("config/colors.yaml")
controllers_config = open_yaml(args.config)

if args.test:
    for i, controller in enumerate(controllers_config["controllers"]):
        controller["url"] = "http://localhost:" + str(6000 + i)

controllers = python.Controllers(controllers_config, args.nosend, VERSION_INFO)
background = python.Background(socketio, controllers)

if __name__ == "__main__":
    if args.background:
        background.startLoop()
    socketio.run(
        app, debug=args.debug, host="0.0.0.0", port=args.port, use_reloader=False
    )
