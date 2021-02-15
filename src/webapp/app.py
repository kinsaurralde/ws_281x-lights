#!/usr/bin/env python3
import json
import logging
import argparse

from collections import OrderedDict

from logging.handlers import RotatingFileHandler
from flask import Flask, json, render_template, request, redirect
from flask_socketio import SocketIO
from engineio.payload import Payload

import coloredlogs
import modules

from version import *

try:
    import yaml  # 3.6
except:  # pragma: no cover
    import ruamel.yaml as yaml  # 3.7

Payload.max_decode_packets = 100

MAX_LOG_BYTES = 4000000

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)-26s:%(funcName)-26s] %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
logging.setLoggerClass(modules.CustomLogger)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

werkzeug_handler = RotatingFileHandler("logs/werkzeug.log", mode="w", maxBytes=MAX_LOG_BYTES, backupCount=2)
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addHandler(werkzeug_handler)
werkzeug_logger.propagate = False

logging.getLogger("urllib3.connectionpool").setLevel("WARNING")

log = logging.getLogger("app")
coloredlogs.DEFAULT_LEVEL_STYLES["info"] = {"color": "black", "bold": True}
coloredlogs.install(level="DEBUG", fmt=LOG_FORMAT, logger=log)
log_file_handler = RotatingFileHandler("logs/app.log", mode="w", maxBytes=MAX_LOG_BYTES, backupCount=3)
log_color_file_handler = RotatingFileHandler("logs/app-color.log", mode="w", maxBytes=MAX_LOG_BYTES, backupCount=3)
log_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
log_color_file_handler.setFormatter(coloredlogs.ColoredFormatter(fmt=LOG_FORMAT))
logging.root.addHandler(log_file_handler)
logging.root.addHandler(log_color_file_handler)
log.setLevel("DEBUG")
log.info("STARTED APP SERVER")

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", help="Debug mode", default=False)
parser.add_argument(
    "-t", "--test", action="store_true", help="Testing mode (localtest)", default=False,
)
parser.add_argument(
    "--nosend", action="store_true", help="Dont send to controllers (For testing)", default=False,
)
parser.add_argument(
    "-c", "--config", type=str, help="Path to controller config", default="config/controllers_sample.yaml",
)
parser.add_argument(
    "-p", "--port", type=int, help="Port to run server on (overrides config file)", default=5000,
)
parser.add_argument(
    "-b", "--background", action="store_false", help="Disable Background Information Thread", default=True,
)
parser.add_argument(
    "--nostart", action="store_true", help="Dont start app", default=False,
)
parser.add_argument(
    "--noschedule", action="store_true", help="Dont start scheduler", default=False,
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


def responsesToDict(responses):
    result = {}
    for response in responses:
        result[response] = responses[response].__dict__
    return result


def responseTemplate(good=False, mtype="", message="", payload={}):  # pylint: disable=dangerous-default-value
    return {"good": good, "type": mtype, "message": message, "payload": payload, "error": not good}


def createResponse(payload, ordered=False):
    """Turn response into json"""
    if ordered:
        payload = OrderedDict(payload)
    try:
        payload = json.dumps(payload, sort_keys=False)
    except TypeError:
        payload = json.dumps(
            {
                "good": False,
                "type": "serialization_error",
                "message": "Failed to serialize response into JSON",
                "payload": {},
            }
        )
    response = app.response_class(response=payload, status=200, mimetype="application/json",)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def error_response(message):
    """Create error response"""
    data = {
        "error": True,
        "message": message,
    }
    return createResponse(data)


@app.before_request
def before_request():
    log.notice(f"[{request.remote_addr}] {request.method} - {request.path}")


@app.after_request
def after_request(response):
    s = (
        f"[{request.remote_addr}] {request.method} - {request.path}"
        f" -> {response.status_code} {response.content_type}"
    )
    if response.status_code == 200:
        log.success(s)
    else:
        log.error(s)
    return response


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
        return createResponse(responseTemplate(good=False, mtype="json_error", message="JSON Decode Error"))
    controllers.setNoSend(getNosend())
    responses = controllers.send(data)
    all_good = responses["all_good"]
    request_responses = responses["responses"]
    response = responseTemplate(all_good, mtype="request_response", payload=responsesToDict(request_responses))
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
    result = controllers.enableController(request.args.get("name"))
    emitUpdatedData()
    response = responseTemplate(not result["error"], "enable_controller", result["message"], result)
    return createResponse(response)


@app.route("/disable")
def disableControllers():
    """Disable selected controller

    Route: /disable

    Methods: GET

    URL Parameters:

        - name: controller name to disable

    Return: JSON
    """
    result = controllers.disableController(request.args.get("name"))
    emitUpdatedData()
    response = responseTemplate(not result["error"], "disable_controller", result["message"], result)
    return createResponse(response)


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


@app.route("/schedule/<mode>")
def scheduleHandler(mode):
    """Start or Stop schedule

    Route: /schedule/<mode>

    Methods: GET

    Mode:

        - start
        - stop

    URL Parameters:

        - schedule: name of schedule
        - function: name of function

    Return: JSON
    """
    schedule = request.args.get("schedule")
    function = request.args.get("function")
    response = {
        "error": False,
        "message": f"{mode} schedule {schedule} with function {function}",
    }
    fail = False
    if mode == "start":
        fail = not scheduler.start(schedule, function)
    elif mode == "stop":
        fail = not scheduler.stop(schedule, function)
    response["error"] = fail
    active_schedules = scheduler.getActiveSchedules()
    socketio.emit("active_schedules", active_schedules)
    return createResponse(response)


@app.route("/getschedules")
def getSchedules():
    """Get list of schedules

    Route: /getschedules

    Methods: GET

    Return: JSON
    """
    active_schedules = scheduler.getActiveSchedules()
    socketio.emit("active_schedules", active_schedules)
    return createResponse(scheduler.getSchedules())


@app.route("/getactiveschedules")
def getActiveSchedules():
    """Get list of active schedules

    Route: /getactiveschedules

    Methods: GET

    Return: JSON
    """
    active_schedules = scheduler.getActiveSchedules()
    socketio.emit("active_schedules", active_schedules)
    return createResponse(active_schedules)


@socketio.on("connect")
def connect():
    log.notice(f"Client Connected: {request.remote_addr}")
    socketio.emit("connection_response", room=request.sid)


@socketio.on("disconnect")
def disconnect():
    log.notice(f"Client Disconnected: {request.remote_addr}")


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


@app.route("/test")
def test():
    return render_template("test.html")


animations_config = open_yaml("config/animations.yaml")
colors_config = open_yaml("config/colors.yaml")
controllers_config = open_yaml(args.config)
sequences_config = open_yaml("config/sequences.yaml")
schedules_config = open_yaml("config/schedules.yaml")

version_info = getVersionInfo()

if args.test:  # pragma: no cover
    for i, controller in enumerate(controllers_config["controllers"]):
        controller["url"] = "http://localhost:" + str(6000 + i)

controllers = modules.Controllers(controllers_config, args.nosend, version_info, socketio)
background = modules.Background(socketio, controllers)
sequencer = modules.Sequencer(socketio, controllers, sequences_config, colors_config)
scheduler = modules.Scheduler(sequencer, schedules_config)

if not args.noschedule:
    scheduler.start_thread()

if __name__ == "__main__" and not args.nostart:  # pragma: no cover
    if args.background:
        background.startLoop()
    socketio.run(app, debug=args.debug, host="0.0.0.0", port=args.port, use_reloader=False)
