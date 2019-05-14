from flask import Flask, render_template, redirect, url_for, json
from controller import *

app = Flask(__name__)

@app.route('/')
def index():
    """Main control page"""
    return render_template('index.html')

@app.route('/off')
@app.route('/<strip_id>/off')
def off(strip_id = 0):
    controller.off(int(strip_id))
    return 'OFF'

@app.route('/stopanimation')
@app.route('/<strip_id>/stopanimation')
def stopanimation(strip_id = 0):
    controller.stop(int(strip_id))
    return 'STOP'

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
    return "/settings/<param>"

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
    controller.stop(strip_id)
    controller.run(int(strip_id), function, params)
    return '/run/function/param'

@app.route('/thread/<function>/<param>')
@app.route('/<strip_id>/thread/<function>/<param>')
def thread(function, param, strip_id = 0):
    params = param.split(",")
    try:
        params = list(map(int, params))
    except ValueError:
        pass
    controller.thread(int(strip_id), function, params)
    return '/thread/function/param'

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
    controller.animate(int(strip_id), function, params, delay)
    return '/animate/<function>/<param>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=200, threaded=True)
