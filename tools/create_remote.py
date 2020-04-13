#!/usr/bin/env python3
import sys
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', type=str, help='Path to source directory (app folder)', default="../app/")
parser.add_argument('-d', '--destination', type=str, help='Path to destination directory (remote_app folder)', default="../remote_app/")
args = parser.parse_args()

if __name__ == "__main__":
    copies = [["py/remote/remote_app.py", "app.py"], ["py/controller.py"], ["py/neopixels.py"], ["py/section.py"]]
    if not os.path.exists(args.source):
        print("App directory", args.source, "does not exist")
        exit(1)
    if os.path.exists(args.destination):
        os.system("rm -rf " + args.destination)
    os.makedirs(args.destination)
    if not os.path.isdir(args.source):
        print("Source path", args.source, "is not a directory")
        exit(1)
    if not os.path.isdir(args.destination):
        print("Destination path", args.destination, "is not a directory")
        exit(1)
    os.makedirs(args.destination + "/py")
    for filename in copies:
        os.system("cp -r " + args.source + filename[0] + " " + args.destination + (filename[1] if len(filename) > 1 else filename[0]))