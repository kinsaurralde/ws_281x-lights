#!/usr/bin/env python3
import json
import time
import argparse
from flask import Flask, request

from controller import NeoPixels, Animations
import version

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--debug", action="store_true", help="Debug mode", default=False
)
parser.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="Testing mode (for non pi devices)",
    default=False,
)
parser.add_argument(
    "-p",
    "--port",
    help="Set port number",
    default=5000,
)
args = parser.parse_args()

app = Flask(__name__)
neo = NeoPixels(testing=args.test)


def create_response(data):
    response = app.response_class(
        response=json.dumps(data), status=200, mimetype="application/json"
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# /**
#  * Route: /
#  * Methods: GET
#  * 
#  * Should only be called for ping or connected check
#  */ 
@app.route("/")
def handleRoot():
    return "Hello!"


# /**
#  * Route: /init
#  * Methods: GET, POST
#  * 
#  * POST JSON Properties:
#  *      - unsigned int id:              id of strip to initialize
#  *      - unsigned int init.brightness: initial brightness value
#  *      - unsigned int init.num_leds:   number of pixels on strip
#  *      - unsigned int init.milliwatts: maximum milliwatts (not implemented)
#  * 
#  * Initialze strip with brightness, number of leds, 
#  */
@app.route("/init", methods=["GET", "POST"])
def init():
    if request.method == 'GET':
        return create_response(neo.getInit())
    return create_response(neo.init(json.loads(request.data)))


# /**
#  * Route: /data 
#  * Methods: POST
#  * 
#  * Parameters:
#  *      - Array of commands, command properties in docs
#  * 
#  * Run animation commands
#  */
@app.route("/data", methods=["POST"])
def handleData():
    print("Data" , request.data)
    neo.handleData(json.loads(request.data))
    return "[]"


# /**
#  * Route: /brightness
#  * Methods: GET
#  * 
#  * Query Parameters:
#  *      - unsigned integer id:    which strip to read/change
#  *      - unsigned integer value: new brightness value (optional)
#  * 
#  * Sets brightness of strip id to value (if exists) then returns current value
#  */
@app.route("/brightness")
def handleBrightness():
    return create_response(neo.handleBrightness(request.args.get('id'), request.args.get('value')))


# /**
#  * Route: /getpixels 
#  * Methods: GET
#  * 
#  * Returns json array of each pixel for each strip
#  */
@app.route("/getpixels")
def handleGetPixels():
    return create_response(neo.getPixels())


# /**
#  * Route: /versioninfo 
#  * Methods: GET
#  * 
#  * Return version info of this controller
#  */
@app.route("/versioninfo")
def versioninfo():
    return create_response({
        "major": version.MAJOR,
        "minor": version.MINOR,
        "patch": version.PATCH,
        "esp_hash": version.ESP_HASH,
        "rpi_hash": version.RPI_HASH,
    })


# /**
#  * Route:
#  * Methods: GET
#  * 
#  * Not used for this controller
#  */
@app.route("/heapfree")
def handleFreeHeap():
    return "-1"


# /**
#  * Route:
#  * Methods: GET
#  * 
#  * Not used for this controller
#  */
@app.route("/ledon")
def ledon():
    return "On"


# /**
#  * Route:
#  * Methods: GET
#  * 
#  * Not used for this controller
#  */
@app.route("/ledoff")
def ledoff():
    return "Off"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=args.port, threaded=True)
