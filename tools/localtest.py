#!/usr/bin/env python3
import argparse
import time
import subprocess
import atexit

try:
    import yaml  # 3.6
except:
    import ruamel.yaml as yaml  # 3.7

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--config", type=str, help="Path to config file", default="configs/localtest.yaml",
)
parser.add_argument("-b", "--buildfolder", type=str, help="Path to buildfolder", default="../build/")
args = parser.parse_args()


def load_yaml(path):
    with open(path) as open_file:
        return yaml.safe_load(open_file)


def createControllerServer(port):
    print(f"Creating controller server on port {port}")
    subprocess.run(
        [args.buildfolder + "raspberrypi/rpi_startup.sh", "--test", "--port", str(port),], check=True,
    )


def createWebappServer():
    print("Creating webapp server")
    command = ["sudo", "python3", "app.py", "--test", "--debug"]
    subprocess.run(command, cwd=f"{args.buildfolder + 'webapp'}", check=True)


def shutdownServers(name):
    print(f"Shutdown {name} servers")
    command = (
        "sudo screen -ls "
        + name
        + " | grep -E '\s+[0-9]+\.' | awk -F ' ' '{print $1}' | "
        + "while read s; do sudo screen -XS $s quit; done"
    )
    subprocess.run(command, shell=True, check=True)


def setup():
    config = load_yaml(args.config)
    webapp_config_name = config["webapp_config"]
    webapp_config = load_yaml(args.buildfolder + "webapp/config/controllers_" + webapp_config_name + ".yaml")
    for i in range(len(webapp_config["controllers"])):
        if webapp_config["controllers"][i]["active"] == "active":
            createControllerServer(6000 + i)
    time.sleep(3)
    createWebappServer()


@atexit.register
def cleanup():
    shutdownServers("rgb_server")


if __name__ == "__main__":
    setup()
