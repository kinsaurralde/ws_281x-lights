from flask import Flask, render_template, redirect, url_for, json, request
from key import Keys
from controller import Controller
import json, sys

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
        data = []
        data.append(controller.info())
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


@app.route('/<key>/off')
@app.route('/<key>/<strip_id>/off')
def off(key, strip_id=0):
    try:
        keys.check_key(key, strip_id)
        controller_response = controller.off(int(strip_id))
    except Exception as e:
        return exception_handler(e)
    return create_response(controller_response)


@app.route('/<key>/stopanimation')
@app.route('/<key>/<strip_id>/stopanimation')
def stopanimation(key, strip_id=0):
    controller_response = controller.stop(int(strip_id))
    return create_response(controller_response)


@app.route('/settings/<param>')
def change_settings(param):
    settings = param.split(",")
    for setting in settings:
        current = setting.split("=")
        if current[0] == "break":
            if current[1] == "true":
                controller.set_break_animation(True)
            else:
                controller.set_break_animation(False)
        if current[0] == "brightness":
            controller.set_brightness(int(current[1]))
    return create_response({})


@app.route('/<key>/<strip_id>/run/<function>')
@app.route('/<key>/<strip_id>/run/<function>/<param>')
def run(key, strip_id, function, param=None):
    try:
        keys.check_key(key, strip_id)
        params = []
        try:
            params = param.split(",")
            params = list(map(int, params))
        except:
            if param == None:
                params = None
        controller.stop(int(strip_id))
        controller_response = controller.run(int(strip_id), function, params)
        return create_response(controller_response)
    except Exception as e:
        return exception_handler(e)


@app.route('/<key>/<strip_id>/thread/<function>/<param>')
def thread(key, strip_id, function, param):
    try:
        keys.check_key(key, strip_id)
        params = param.split(",")
        try:
            params = list(map(int, params))
        except ValueError:
            pass
        controller_response = controller.thread(
            int(strip_id), function, params)
        return create_response(controller_response)
    except Exception as e:
        return exception_handler(e)

@app.route('/<key>/<strip_id>/animate/<function>/<param>')
@app.route('/<key>/<strip_id>/animate/<function>/<param>/<delay>')
def animate(key, strip_id, function, param, delay=0):
    try:
        keys.check_key(key, strip_id)
        params = param.split(",")
        try:
            params = list(map(int, params))
        except ValueError:
            pass
        controller.stop(int(strip_id))
        controller_response = controller.animate(
            int(strip_id), function, params, delay)
        return create_response(controller_response)
    except Exception as e:
        return exception_handler(e)

@app.route('/json', methods=['GET', 'POST'])
def post_json():
    data = request.get_json()
    return create_response(controller.from_json(data))


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
