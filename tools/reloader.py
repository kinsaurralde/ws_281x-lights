#!/usr/bin/env python3
import os
import signal
import threading
import argparse
import subprocess
import multiprocessing

from flask import Flask, render_template
app = Flask(__name__)

parser = argparse.ArgumentParser()
# parser.add_argument('-p', '--path', type=str, help='Path to config directory', required=True)
# parser.add_argument('-a', '--app-path', type=str, help='Path to app directory', default="../app/")
# parser.add_argument('-c', '--clear', action='store_true', help='Delete tmp directory', default=False)
parser.add_argument('-p', '--port', type=int, help='Port to listen on', default=5002)
parser.add_argument('-s', '--startup', type=str, help='Path to startup', default='startup.sh')
args = parser.parse_args()

run_process = None
run_thread = None

def run(path):
    global run_process
    run_process = subprocess.run(["./../app/app.py", "-t"], cwd="../app")

@app.route('/')
def index():
    return "LOL"

@app.route('/start')
def start():
    global run_process
    # run_process = subprocess.Popen(["./" + args.startup], close_fds=True)
    run_process = multiprocessing.Process(target=run, args=[args.startup])
    run_process.start()
    return "Started"

@app.route('/stop')
def stop():
    global run_process
    print("process", run_process)
    if run_process is not None:
        run_process.terminate()
        run_process.join()
    return "Stopped"

if not os.path.exists(args.startup):
    print("Startup file", args.startup, "does not exist!")
    exit(1)

# app.run(port=args.port, debug=False)
