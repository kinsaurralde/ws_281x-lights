#!/usr/bin/env python3
import json
import argparse

from collections import OrderedDict

from flask import Flask, json, render_template, request, redirect
from flask_socketio import SocketIO
from engineio.payload import Payload

import modules

from version import *

try:
    import yaml  # 3.6
except:  # pragma: no cover
    import ruamel.yaml as yaml  # 3.7

Payload.max_decode_packets = 100

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
    "-s",
    "--pixel-simulate",
    action="store_true",
    help="Simulate pixels",
    default=False,
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


def getVersionInfo():
    """Get version info"""
    return {
        "major": MAJOR,
        "minor": MINOR,
        "patch": PATCH,
        "label": LABEL,
        "esp_hash": ESP_HASH,
        "rpi_hash": RPI_HASH,
    }


def getNosend():
    return args.nosend


def open_yaml(path):
    """Open yaml file and return as a dictionary"""
    data = {}
    with open(path) as open_file:
        data = yaml.safe_load(open_file)
    return data


def createResponse(data, ordered=False):
    """Turn response into json"""
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
    """Create error response"""
    data = {
        "error": True,
        "message": message,
    }
    return createResponse(data)


@app.errorhandler(404)
def page_not_found(e):
    return error_response(str(e)), 404


@app.route("/")
def index():
    """Render main control page

    Route: /

    Methods: GET

    Return: webpage
    """
    return render_template("index.html")


@app.route("/data", methods=["POST"])
def handleData():
    """Recieve JSON array of commands then send to controllers

    Route: /data

    Methods: POST

    Return: JSON
    """
    data = []
    try:
        data = json.loads(request.data)
    except ValueError:
        response = {"error": True, "message": "JSON Decode Error"}
        return createResponse(response)
    controllers.setNoSend(getNosend())
    fails = controllers.send(data)
    response = {"error": len(fails) > 0, "message": fails}
    return createResponse(response)


@app.route("/docs")
def docs():
    """Redirect to documentation on Github

    Route: /docs

    Methods: GET

    Return: redirect to webpage
    """
    return redirect("https://kinsaurralde.github.io/ws_281x-lights/#/")


@app.route("/getanimations")
def getanimations():
    """Return animations config
    Route: /getanimations

    Methods: GET

    Return: JSON
    """
    return createResponse(animations_config)


@app.route("/getcolors")
def getcolors():
    """Return colors config

    Route: /getcolors

    Methods: GET

    Return: JSON
    """
    return createResponse(colors_config)


@app.route("/getcontrollers")
def getcontrollers():
    """Return controllers config

    Route: /getcontrollers

    Methods: GET

    Return: JSON
    """
    return createResponse(controllers.getConfig(), True)


@app.route("/getversioninfo")
def getversioninfo():
    """Return controller version information

    Route: /getversioninfo

    Methods: GET

    Return: JSON
    """
    return createResponse(controllers.getControllerVersionInfo())


@app.route("/getinitialized")
def getinitialized():
    """Return controller initialization status

    Route: /getinitialized

    Methods: GET

    Return: JSON
    """
    return createResponse(controllers.getControllerInitialized())


@app.route("/enable")
def enableControllers():
    """Enable selected controller

    Route: /enable

    Methods: GET

    URL Parameters:

        - name: controller name to enable

    Return: JSON
    """
    fails = controllers.enableController(request.args.get("name"))
    emitUpdatedData()
    return createResponse({"error": len(fails) > 0, "message": fails})


@app.route("/disable")
def disableControllers():
    """Disable selected controller

    Route: /disable

    Methods: GET

    URL Parameters:

        - name: controller name to disable

    Return: JSON
    """
    fails = controllers.disableController(request.args.get("name"))
    emitUpdatedData()
    return createResponse({"error": len(fails) > 0, "message": fails})


@app.route("/update")
def update():
    """Get update data (ping, etc)

    Route: /update

    Methods: GET

    Return: String (undefined)
    """
    emitUpdatedData()
    return "Emitted"


@app.route("/getpixels")
def getPixels():
    """Get current pixel colors (simulated)

    Route: /getpixels

    Methods: GET

    Return: JSON
    """
    return createResponse(controllers.getPixels())


@app.route("/getpixelsimulate")
def getPixelSimulate():
    """Get pixel simulate data

    Route: /getpixelsimulate

    Methods: GET

    Return: JSON
    """
    return {
        "active": args.pixel_simulate,
        "controllers": controllers.getControllerSizes(),
    }


@app.route("/setpixelemit")
def setPixelInterval():
    """Set pixel emit config

    Route: /setpixelemit

    Methods: GET

    URL Parameters:

        - active: (bool) enable/disable pixel emit
        - interval: (int) set time between emits in ms

    Return: JSON
    """
    active = request.args.get("active")
    interval = request.args.get("interval")
    if active is not None:
        background.setPixelsActive(active)
    if interval is not None:
        background.setPixelInterval(int(interval))
    return {
        "active": background.getPixelsActive(),
        "interval": background.getPixelInterval(),
    }


@app.route("/sequence/<mode>")
def sequenceHandler(mode):
    """Start Stop or Toggle sequence

    Route: /sequence/<mode>

    Methods: GET

    Mode:

        - start
        - toggle
        - stop

    URL Parameters:

        - sequence: name of sequence
        - function: name of function
        - iterations: number of iterations (default: None (infinite))

    Return: JSON
    """
    sequence = request.args.get("sequence")
    function = request.args.get("function")
    iterations = request.args.get("iterations", None)
    response = {
        "error": False,
        "message": f"{mode} sequence {sequence} with function {function} {iterations} times",
    }
    fail = False
    if mode == "start":
        fail = not sequencer.run(sequence, function, iterations)
    elif mode == "toggle":
        # fail = not sequencer.toggle(sequence, function, iterations)
        fail = True
    elif mode == "stop":
        fail = not sequencer.stop(sequence, function)
    response["error"] = fail
    return createResponse(response)


@app.route("/sequence/stopall")
def sequenceStopAll():
    """Stop all running sequences

    Route: /sequence/stopall

    Methods: GET

    Return: String (undefined)
    """
    sequencer.stopAll()
    return "Stopped"


@app.route("/getsequences")
def getsequences():
    """Get list of sequences

    Route: /getsequences

    Methods: GET

    Return: JSON
    """
    return createResponse(sequencer.getSequences())


@socketio.on("connect")
def connect():
    print("Client Connected:", request.remote_addr)
    socketio.emit("connection_response", room=request.sid)


@socketio.on("disconnect")
def disconnect():
    print("Client Disconnected")


@socketio.on("webpage_loaded")
def webapgeLoaded():
    emitUpdatedData()
    last_brightness = controllers.getLastBrightness()
    brightness = []
    for name in last_brightness:
        brightness.append({"name": name, "value": last_brightness[name]})
    socketio.emit("brightness", brightness)


@socketio.on("set_brightness")
def setBrightness(json):
    controllers.brightness(json)
    socketio.emit("brightness", json)


def emitUpdatedData():
    background.updatePing()
    background.updateData()
    background.emitUpdate()


animations_config = open_yaml("config/animations.yaml")
colors_config = open_yaml("config/colors.yaml")
controllers_config = open_yaml(args.config)
sequences_config = open_yaml("config/sequences.yaml")
schedules_config = open_yaml("config/schedules.yaml")

if args.test:  # pragma: no cover
    for i, controller in enumerate(controllers_config["controllers"]):
        controller["url"] = "http://localhost:" + str(6000 + i)

controller_module = None
if args.pixel_simulate:
    import controller as controller_module

controllers = modules.Controllers(
    controllers_config, args.nosend, getVersionInfo(), controller_module
)
background = modules.Background(socketio, controllers, args.pixel_simulate)
sequencer = modules.Sequencer(socketio, controllers, sequences_config, colors_config)
scheduler = modules.Scheduler(sequencer, schedules_config)

if __name__ == "__main__":  # pragma: no cover
    if args.background:
        background.startLoop()
    socketio.run(
        app, debug=args.debug, host="0.0.0.0", port=args.port, use_reloader=False
    )
