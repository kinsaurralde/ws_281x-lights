#!/usr/bin/env python3
import tempfile
import argparse
import subprocess

try:
    import yaml  # 3.6
except:
    import ruamel.yaml as yaml  # 3.7

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    type=str,
    help="Path to config file",
    default="configs/upload_rpi.yaml",
)
parser.add_argument(
    "-b", "--buildfolder", type=str, help="Path to buildfolder", default="../build/"
)
args = parser.parse_args()


def load_yaml(path):
    with open(path) as open_file:
        return yaml.safe_load(open_file)


def send(device):
    folder = None
    if device["controller"]:
        folder = args.buildfolder + "raspberrypi/"

    if folder is not None:
        # print(folder, device)
        with tempfile.NamedTemporaryFile() as tf:
            tf.write(bytes("cd " + device["destination"] + "\n", "utf-8"))
            tf.write(bytes("put -r " + folder + "\n", "utf-8"))
            tf.flush()
            subprocess.run(  # pylint: disable=no-member
                ["sftp", "-i", device["key"], "-b", tf.name, device["userhost"]],
                check=True,
            )


if __name__ == "__main__":
    devices = load_yaml(args.config)
    for device in devices:
        send(device)
