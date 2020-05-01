#!/usr/bin/env python3
import os
import tempfile
import argparse
import subprocess

try:
    import yaml # 3.6
except:
    import ruamel.yaml as yaml  # 3.7

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, help='Path to config directory', required=True)
parser.add_argument('-a', '--app-path', type=str, help='Path to app directory', default="../app/")
parser.add_argument('-c', '--clear', action='store_true', help='Delete tmp directory', default=False)
args = parser.parse_args()

def load_yaml(path):
    with open(path) as open_file:
        return yaml.load(open_file)

def send(device):
    login = device["user"] + "@" + device["hostname"]
    folder = "tmp/remote_app/" if device["remote"] else "tmp/app/"
    if not device["remote"]:
        subprocess.run(["cp", "-r", args.path + "/app/", "tmp/app/configs/generated"])
        with open("tmp/app/startup.sh", "w") as startup:
            startup.write("sudo screen -dmS rgb_app python3 app.py -c configs/generated/main.yaml\n")
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(bytes('cd ' + device["path"] + '\nput -r ' + folder, 'utf-8'))
        tf.flush()
        subprocess.run(["sftp", "-i", device["ssh"], "-b", tf.name, login])

if __name__ == "__main__":
    subprocess.run(["rm", "-rf", "tmp/"])
    subprocess.run(["mkdir", "tmp"])
    subprocess.run(["cp", "-r", args.app_path, "tmp/app/"])
    subprocess.run(["./create_remote.py", "-s", args.app_path])
    # subprocess.run(["find", "-name",  "__pycache__", "-exec", "rm", "-rf", '"{}"', "\;"])
    devices = load_yaml(args.path + "/devices.yaml")
    for device in devices["devices"]:
        send(device)
    if args.clear:
        subprocess.run(["rm", "-rf", "tmp/"])
        subprocess.run(["mkdir", "tmp"])
