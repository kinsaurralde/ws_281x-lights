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

import packet_pb2 as proto_packet

Payload.max_decode_packets = 100

MAX_LOG_BYTES = 4000000
ESP_IP_ADDRESS = "10.0.0.72"

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)-26s:%(funcName)-26s] %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
modules.addCustomLogLevels()

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
parser.add_argument("--ping-controllers", action="store_true", help="Send a ping to controllers every 15 seconds")
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
coloredlogs.DEFAULT_LEVEL_STYLES["esp"] = {"color": "cyan", "faint": True}

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


class Global:
    def __init__(self, socketio, presets_config, controllers_config, sequences_config) -> None:
        animation_config = presets_config.get("animations", None)
        animation_args_config = presets_config.get("animation_args", None)
        colors_config = presets_config.get("colors", None)
        if animation_config is None or animation_args_config is None or colors_config is None:
            log.critical("Incomplete presets config")
            raise Exception("Incomplete presets config")
        # 1st init group
        self.socketio = socketio
        self.colors = modules.Colors(colors_config)
        self.controllers = modules.Controllers(controllers_config)
        # 2nd init group
        self.animations = modules.Animations(self.colors, self.controllers, animation_config, animation_args_config)
        self.packet_manager = modules.PacketManager(self.socketio, self.controllers)
        # 3rd init group
        self.sequencer = modules.Sequencer(self, sequences_config)


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
    return render_template("mobile.html.jinja", defaults=presets_config_file["web_options"])


@app.route("/pwalayout")
def pwaLayout():
    return modules.createResponse(app, presets_config_file)


@app.route("/controllers")
def getControllers():
    return modules.createResponse(app, controllers_config_file)


@app.route("/controllerstartup", methods=["POST"])
def controllerStartUp():
    remote_ip_addr = request.remote_addr
    log.info(f"Controller startup: {remote_ip_addr}")
    g.packet_manager.send(remote_ip_addr, g.controllers.createControllerInitMessage(remote_ip_addr, args.port))
    return ""


@app.route("/version")
def getversion():
    g.packet_manager.getVersion()
    return ""


@app.route("/controllersdebug")
def controllersDebug():
    g.packet_manager.getESPInfo()
    return ""


@socketio.on("animation")
def handleAnimation(data):
    log.notice(f"Recieved socketio 'animation': {data}")
    payloads = g.animations.createAnimationPayload(data)
    g.packet_manager.sendList(payloads)


@socketio.on("ledinfo")
def handleBrightness(data):
    log.info(f"Recieved socketio 'ledinfo': {data}")
    socketio.emit("ledinfo", data)
    ips = g.controllers.getControllerIps(data.get("controllers", []))
    payload = g.packet_manager.createLEDInfoPayload(data)
    options = proto_packet.Options()
    options.send_ack = False
    for ip in ips:
        g.packet_manager.send(ip, payload, options)


@socketio.on("sequence_start")
def handleSequenceStart(data):
    log.notice(f"Recieved socketio 'sequence_start': {data}")
    # sequencer


@socketio.on("connect")
def connect():
    log.notice(f"Client Connected: {request.remote_addr}")
    socketio.emit("connection_response", room=request.sid)


@socketio.on("disconnect")
def disconnect():
    log.notice(f"Client Disconnected: {request.remote_addr}")


try:
    remote_log_manager = modules.RemoteLogManager()
    remote_log_manager.start()
    presets_config_file = modules.openYamlBackup("config/presets.yaml", "config/example.presets.yaml")
    controllers_config_file = modules.openYamlBackup(args.controller_config, "config/exmaple.controllers.yaml")
    sequences_config_file = modules.openYamlBackup("config/sequences.yaml", "config/example.sequences.yaml")

    log.info(f"Presets Config: {presets_config_file}")
    log.info(f"Controllers Config: {controllers_config_file}")
    log.info(f"Sequences Config: {sequences_config_file}")

    g = Global(socketio, presets_config_file, controllers_config_file, sequences_config_file)

    g.packet_manager.setVersion(version.MAJOR, version.MINOR, version.PATCH)
    g.packet_manager.registerIps(g.controllers.getAllControllerIps())
    g.packet_manager.sendList(g.controllers.createAllControllerInitMessages(args.port))
    if not args.background_disabled:
        g.packet_manager.startBackgroundThread()
    if args.ping_controllers:
        g.packet_manager.setPingInterval(args.ping_interval)
        g.packet_manager.startPingThread()

    metrics_dashboard = dash.Dash(__name__, server=app, url_base_pathname="/dashboard/")
    dashapp.setup.setup(app, metrics_dashboard, g.packet_manager)
except Exception as e:  # pylint: disable=broad-except
    logging.critical(f"Setup failed: {e}", exc_info=True)
    sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    if not args.flask_nostart:
        socketio.run(app, debug=args.flask_debug, host="0.0.0.0", port=args.port, use_reloader=False)
