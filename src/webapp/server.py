import sys
import logging
import argparse
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from engineio.payload import Payload

import coloredlogs
import dash
import dashapp.setup
import modules
import version
import config

Payload.max_decode_packets = 100

MAX_LOG_BYTES = 4000000
ESP_IP_ADDRESS = "10.0.0.72"

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)-26s:%(funcName)-26s] %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
logging.setLoggerClass(modules.CustomLogger)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

parser = argparse.ArgumentParser()

parser.add_argument("--logging-dont-save", action="store_true", help="Disable saving logs to files")
parser.add_argument("--logging-max-bytes-per-file", type=int, help="Maximum bytes per log file", default=4000000)
parser.add_argument("--logging-backup-count", type=int, help="Amount of backup log files in rotation", default=3)

parser.add_argument("--flask-debug", action="store_true", help="Enable Flask Debug mode")
parser.add_argument("--flask-nostart", action="store_true", help="Dont start flask app")
parser.add_argument("-p", "--port", type=int, help="Port to run server on", default=80)

parser.add_argument(
    "-c", "--controller-config", type=str, help="Path to controller config", default="config/controllers.yaml",
)
parser.add_argument(
    "-b", "--background-disabled", action="store_true", help="Disable main background thread", default=False,
)
parser.add_argument(
    "--background-interval",
    type=int,
    help="Number of seconds between main background thread runs",
    default=config.DEFAULT_BACKGROUND_INTERVAL,
)
parser.add_argument("--ping-controllers", action="store_true", help="Send a ping to controllers every 5 seconds")
parser.add_argument(
    "--ping-interval",
    type=int,
    help="Number of seconds between pings to controllers",
    default=config.DEFAULT_PING_INTERVAL,
)

args = parser.parse_args()

werkzeug_handler = RotatingFileHandler("logs/werkzeug.log", mode="a", maxBytes=MAX_LOG_BYTES, backupCount=2)
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addHandler(werkzeug_handler)
werkzeug_logger.propagate = False

logging.getLogger("urllib3.connectionpool").setLevel("WARNING")

log = logging.getLogger("app")
coloredlogs.DEFAULT_LEVEL_STYLES["info"] = {"color": "black", "bold": True}
coloredlogs.install(level="DEBUG", fmt=LOG_FORMAT, logger=log)
log_file_handler = RotatingFileHandler(
    "logs/app.log", mode="a", maxBytes=args.logging_max_bytes_per_file, backupCount=args.logging_backup_count
)
log_color_file_handler = RotatingFileHandler(
    "logs/app-color.log", mode="a", maxBytes=args.logging_max_bytes_per_file, backupCount=args.logging_backup_count
)
log_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
log_color_file_handler.setFormatter(coloredlogs.ColoredFormatter(fmt=LOG_FORMAT))
logging.root.addHandler(log_file_handler)
logging.root.addHandler(log_color_file_handler)
log.setLevel("INFO")
log.info("STARTED APP SERVER")

log.notice(f"Parsed Args: {args}")


@app.before_request
def beforeRequest():
    log.notice(f"[{request.remote_addr}] {request.method} - {request.path}")


@app.after_request
def afterRequest(response):
    message = (
        f"[{request.remote_addr}] {request.method} - {request.path}"
        f" -> {response.status_code} {response.content_type}"
    )
    if response.status_code == 200:
        log.success(message)
    else:
        log.error(message)
    return response


@app.errorhandler(404)
def pageNotFound(error):
    return modules.errorResponse(app, str(error)), 404


@app.route("/")
def root():
    return render_template("mobile.html.jinja", defaults=presets_config["web_options"])


@app.route("/pwalayout")
def pwaLayout():
    return modules.createResponse(app, presets_config)


@app.route("/controllers")
def getControllers():
    return modules.createResponse(app, controllers_config)


@app.route("/controllerstartup", methods=["POST"])
def controllerStartUp():
    remote_ip_addr = request.remote_addr
    log.info(f"Controller startup: {remote_ip_addr}")
    pm.send(remote_ip_addr, controllers.createControllerInitMessage(remote_ip_addr))
    return ""


@app.route("/version")
def getversion():
    pm.getVersion()
    return ""


@app.route("/controllersdebug")
def controllersDebug():
    pm.getESPInfo()
    return ""


@socketio.on("animation")
def handleAnimation(data):
    log.notice(f"Recieved socketio 'animation': {data}")
    payloads = animations.createAnimationPayload(data)
    for payload in payloads:
        pm.send(ESP_IP_ADDRESS, payload)


@socketio.on("ledinfo")
def handleBrightness(data):
    log.info(f"Recieved socketio 'ledinfo': {data}")
    socketio.emit("ledinfo", data)
    payload = pm.createLEDInfoPayload(data)
    pm.send(ESP_IP_ADDRESS, payload)


@socketio.on("connect")
def connect():
    log.notice(f"Client Connected: {request.remote_addr}")
    socketio.emit("connection_response", room=request.sid)


@socketio.on("disconnect")
def disconnect():
    log.notice(f"Client Disconnected: {request.remote_addr}")


try:
    presets_config = modules.openYaml("config/presets.yaml")
    controllers_config = modules.openYaml(args.controller_config)

    log.notice(f"Presets Config: {presets_config}")
    log.notice(f"Controllers Config: {controllers_config}")

    controllers = modules.Controllers(controllers_config)

    pm = modules.PacketManager(socketio, controllers, presets_config)
    pm.setVersion(version.MAJOR, version.MINOR, version.PATCH)
    pm.registerIps(controllers.getControllerIps())
    pm.sendList(controllers.createAllControllerInitMessages())
    if not args.background_disabled:
        pm.startBackgroundThread()
    if args.ping_controllers:
        pm.startPingThread()

    colors = modules.Colors()
    colors.addColors(presets_config["colors"])

    animations = modules.Animations(colors, presets_config)

    metrics_dashboard = dash.Dash(__name__, server=app, url_base_pathname="/dashboard/")
    dashapp.setup.setup(app, metrics_dashboard, pm)
except Exception as e:  # pylint: disable=broad-except
    logging.critical(f"Setup failed: {e}", exc_info=True)
    sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    socketio.run(app, debug=args.flask_debug, host="0.0.0.0", port=args.port, use_reloader=False)
