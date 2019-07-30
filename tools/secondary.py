#!/usr/bin/env python3
import sys
import os
import shutil


def update(folder_name):
    if os.path.isdir(folder_name):
        print(folder_name)
        shutil.copy("../app.py", folder_name + "app.py")
        shutil.copy("../key.py", folder_name + "key.py")
        shutil.copy("../controller.py", folder_name + "controller.py")
        shutil.copy("../lights.py", folder_name + "lights.py")


def create_new(folder_name):
    files = os.listdir(folder_name)
    folder_name += "/"
    [files.remove(file) for file in files if len(file.split('.')) <
     2 or file.split('.')[1] != "json"]  # dont use non .json files
    for file in files:
        cur_folder = folder_name + file.split('.')[0] + "/"
        if not os.path.exists(cur_folder):
            os.makedirs(cur_folder)
        shutil.copy(folder_name + file, cur_folder + "config.json")
        startup_script = "sudo screen -S rgb sudo python3 app.py config.json"
        with open(cur_folder + "startup.sh", "w") as startup_file:
            os.chmod(cur_folder + "startup.sh", 0o755)
            startup_file.write(startup_script)
        update(cur_folder)


if len(sys.argv) < 3:
    print("Usage: ./secondary.py <mode> <path>")
    exit(1)

folder_name = sys.argv[2]
if not os.path.exists(folder_name):
    print("Path", folder_name, "does not exist")

if sys.argv[1] == "new":
    create_new(folder_name)
elif sys.argv[1] == "update":
    folders = os.listdir(folder_name)
    folder_name += "/"
    for folder in folders:
        if os.path.isdir(folder_name + folder):
            update(folder_name + folder + "/")
else:
    print("Mode options are: new or update")
    exit(1)
