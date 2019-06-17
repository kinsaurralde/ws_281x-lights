from flask import Flask, render_template, redirect, url_for, json
from controller import *

app = Flask(__name__)

def create_response(data):
    return app.response_class(response = json.dumps(data), status = 200, mimetype = 'application/json')
    
@app.route('/')
def index():
    """Main control page"""
    return render_template('index.html')

@app.route('/off')
@app.route('/<strip_id>/off')
def off(strip_id = 0):
    controller_response = controller.off(int(strip_id))
    return create_response(controller_response)

@app.route('/stopanimation')
@app.route('/<strip_id>/stopanimation')
def stopanimation(strip_id = 0):
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

@app.route('/run/<function>')
@app.route('/run/<function>/<param>')
@app.route('/<strip_id>/run/<function>/<param>')
def run(function, param = None, strip_id = 0):
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

@app.route('/thread/<function>/<param>')
@app.route('/<strip_id>/thread/<function>/<param>')
def thread(function, param, strip_id = 0):
    params = param.split(",")
    try:
        params = list(map(int, params))
    except ValueError:
        pass
    controller_response = controller.thread(int(strip_id), function, params)
    return create_response(controller_response)

@app.route('/animate/<function>/<param>')
@app.route('/animate/<function>/<param>/<delay>')
@app.route('/<strip_id>/animate/<function>/<param>')
@app.route('/<strip_id>/animate/<function>/<param>/<delay>')
def animate(function, param, strip_id = 0, delay = 0):
    params = param.split(",")
    try:
        params = list(map(int, params))
    except ValueError:
        pass
    controller.stop(strip_id)
    controller_response = controller.animate(int(strip_id), function, params, delay)
    return create_response(controller_response)

controller = Controller(0)

controller.run(0, "wipe", (255, 0, 0, 1, 1))
controller.run(0, "wipe", (0, 255, 0, 1, 1))
controller.run(0, "wipe", (0, 0, 255, 1, 1))
controller.run(0, "wipe", (0, 0, 0, 1, 1))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=200, threaded=True)
