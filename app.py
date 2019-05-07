from flask import Flask, render_template, redirect, url_for, json
from lights import *
from time import sleep
import sys
import threading

app = Flask(__name__)

# Routes


@app.route('/')
def index():
    """Main control page"""
    return render_template('index.html')


@app.route('/run/<function>/<param>')
def run(function, param):
    """Non repeating functions"""
    end_animation()
    params = param.split(",")
    if function == "color":  # set entire strip to given color
        set_color(int(params[0]), int(params[1]), int(params[2]))
    elif function == "random":
        set_random((int(params[0]), int(params[1])))
    elif function == "wipe":
        set_wipe(int(params[0]), int(params[1]), int(
            params[2]), int(params[3]), int(params[4]))
    elif function == "chase": # REMOVE
        set_chase(int(params[0]), int(params[1]), int(
            params[2]), int(params[3]), int(params[4]))
    elif function == "single":
        set_light(int(params[0]), int(params[1]),
                  int(params[2]), int(params[3]))
    elif function == "pulse":
        lights_pulse(int(params[0]), int(params[1]), int(
            params[2]), int(params[3]), int(params[4]), int(params[5]), animation_id.get())
    elif function == "specific":
        set_specific(params)
    return "/run/<function>/<param>"


@app.route('/animate/<function>/<param>')
def animation(function, param):
    """Repeating functions"""
    params = param.split(",")
    end_animation()
    if function == "stop": # REMOVE
        end_animation()
        set_color(0, 0, 0)
        return "Animation Stopped"
    elif function == "chase":
        execute = animation_chase
        arguments = (int(params[0]), int(params[1]),
                     int(params[2]), int(params[3]))
    elif function == "rainbowCycle":
        execute = animation_rainbow_cycle
        arguments = (int(params[0]),)
    elif function == "rainbowChase":
        execute = animation_rainbow_chase
        arguments = (int(params[0]),)
    elif function == "random":
        execute = animation_random_cycle
        arguments = (int(params[0]), int(params[1]))
    elif function == "shift":
        execute = animation_shift
        arguments = (int(params[0]), int(params[1]))
    elif function == "pulse":
        execute = animation_pulse
        arguments = (int(params[0]), int(params[1]),
                     int(params[2]), int(params[3]),
                     int(params[4]), int(params[5]),
                     int(params[6]), int(params[7]))
    elif function == "mix":
        execute = animation_mix_colors
        colors = []
        for i in range(1, len(params)):
            current = params[i].split(".")
            next_color = (int(current[0]), int(current[1]), int(current[2]))
            colors.append(next_color)
        arguments = (float(params[0]), colors)
    lights_process(execute, arguments)
    return "/animate/<function>/<param>"


@app.route('/operations/<function>/<param>')
def operations(function, param):
    """Shifting / Reversing"""
    params = param.split(",")
    if function == "shift":
        lights_shift(int(params[0]), int(params[1]))
    if function == "reverse":
        lights_reverse()
    return "/run/<function>/<param>"


@app.route('/settings/<param>')
def change_settings(param):
    settings = param.split(",")
    for setting in settings:
        current = setting.split("=")
        if current[0] == "break":
            if current[1] == "true":
                global_settings.set_break_animation(True)
            else:
                global_settings.set_break_animation(False)
        if current[0] == "brightness":
            global_settings.set_brightness(int(current[1]))
    return "/settings/<param>"

@app.route('/get')
def get():
    data = state.get_state()
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/stopanimation')
def stopanimation():
    end_animation()
    return "/off"


@app.route('/off')
def off():
    end_animation()
    lights_off()
    return "/off"


@app.route('/reverse')
def reverse():
    lights_reverse()
    return "/reverse"


def set_color(r, g, b):
    lights_set_color(r, g, b)


def set_wipe(r, g, b, direction, wait_ms):
    lights_wipe(r, g, b, direction, wait_ms, animation_id.get())


def set_chase(r, g, b, wait_ms, iterations):
    lights_chase(r, g, b, wait_ms, iterations, animation_id.get())


def animation_chase(arguments):  # r, g, b, wait_ms
    lights_chase(arguments[0], arguments[1], arguments[2],
                 arguments[3], 1, animation_id.get())


def animation_rainbow_cycle(arguments):  # wait_ms
    lights_rainbow_cycle(arguments[0], 1, animation_id.get())


def animation_rainbow_chase(arguments):  # wait_ms
    lights_rainbow_chase(arguments[0], animation_id.get())


def animation_random_cycle(arguments):  # each ,wait_ms
    lights_random_cycle(arguments[0], arguments[1], 1, animation_id.get())


def animation_pulse(arguments):  # r, g, b, direction, wait_ms, length
    if arguments[6] == 1:
        lights_pulse(arguments[0], arguments[1], arguments[2],
                     arguments[3], arguments[4], arguments[5], animation_id.get())
        sleep(arguments[7]/1000.0)
    else: # REMOVE
        print("ANIMATION PULSE")
        lights_pulse(arguments[0], arguments[1], arguments[2],
                     arguments[3], arguments[4], arguments[5], animation_id.get())


def animation_mix_colors(arguments):
    lights_mix_switch(arguments[0], arguments[1], animation_id.get())


def animation_shift(arguments):
    lights_shift(arguments[0], arguments[1])


def set_random(arguments):
    lights_random_cycle(arguments[0], arguments[1], 1, animation_id.get())


def set_light(i, r, g, b):
    lights_set(i, r, g, b)


def set_specific(pixels):
    for pixel in pixels:
        data = pixel.split(".")
        lights_set(int(data[0]), int(data[1]), int(data[2]), int(data[3]))



def lights_process(function, arguments):
    animation_id.increment()
    this_id = animation_id.get()
    while this_id == animation_id.get():
        function(arguments)


def end_animation():
    animation_id.increment()



# Set port from command line arguments
port = 5000
if (len(sys.argv) > 1):
    port = int(sys.argv[1])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
