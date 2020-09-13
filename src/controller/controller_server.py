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


@app.route("/")
def handleRoot():
    return "Hello!"


@app.route("/data", methods=["POST"])
def handleData():
    print("Data" , request.data)
    neo.handleData(json.loads(request.data))
    return "[]"


@app.route("/getpixels")
def handleGetPixels():
    return create_response(neo.getPixels())


@app.route("/heapfree")
def handleFreeHeap():
    return "-1"


@app.route("/brightness")
def handleBrightness():
    return create_response(neo.handleBrightness(request.args.get('id'), request.args.get('value')))

@app.route("/versioninfo")
def versioninfo():
    return create_response({
        "major": version.MAJOR,
        "minor": version.MINOR,
        "patch": version.PATCH,
        "esp_hash": version.ESP_HASH,
        "rpi_hash": version.RPI_HASH,
    })

@app.route("/ledon")
def ledon():
    return "On"

@app.route("/ledoff")
def ledoff():
    return "Off"

@app.route("/init", methods=["POST"])
def init():
    neo.init(json.loads(request.data))
    return "Init"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=args.port, threaded=True)
