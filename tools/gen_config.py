#!/usr/bin/env python3
import sys
import datetime
import json
import os


class Controller():
    def __init__(self):
        self.data = {}

    def load(self, data):
        print("loading")

    def create_new(self, is_primary: bool):
        self.data["primary"] = is_primary
        if not is_primary:
            self.data["remote"] = input("Input remote URL")
        self.physical_strip()
        self.settings()
        self.virtual_strips()
        return self.get_data()

    def physical_strip(self):
        led_count = get_int("Enter number of LEDs on strip: ", 0, 1000)
        max_brightness = get_int(
            "Enter maximum brightness (0 - 255): ", 0, 255)
        max_milliamps = get_int(
            "Enter maximum milliamps entire strip can use: ", 0, 100000)
        volts = get_int("Enter voltage of power supply (5 or 12): ", 5, 12)
        self.data["neopixels"] = {
            "led_count": led_count,
            "max_brightness": max_brightness,
            "max_milliamps": max_milliamps,
            "volts": volts
        }

    def settings(self):
        initial_brightness = get_int(
            "Enter initial brightness: ", 0, self.data["neopixels"]["max_brightness"])
        self.data["settings"] = {
            "initial_brightness": initial_brightness
        }

    def virtual_strips(self):
        self.data["strips"] = []
        while get_bool("Add a virtual strip?"):
            start = get_int("Enter first pixel id: ", 0,
                            self.data["neopixels"]["led_count"])
            end = get_int("Enter last pixel id: ", start,
                          self.data["neopixels"]["led_count"])
            current = {
                "start": start,
                "end": end
            }
            self.data["strips"].append(current)

    def get_data(self):
        return self.data


def get_int(message: str, min: int, max: int):
    """Gets positive integer between or equal to min and max from user input"""
    value = -1
    while value < 0 or value < min or value > max:
        temp = input(message)
        if temp.isdecimal():
            value = int(temp)
    return int(value)


def get_bool(message):
    value = "a"
    while value != "y" and value != "n":
        value = input(message + " (y or n): ").lower()
    if value == "y":
        return True
    else:
        return False


def ask_controllers():
    data = []
    more_controllers = True
    is_primary = True
    while more_controllers:
        current = Controller()
        data.append(current.create_new(is_primary))
        is_primary = False
        more_controllers = get_bool("Add another (remote) controller?")
    return data


def ask_keys():
    data = {}
    web_key = input("Enter Web Key: ")
    while web_key.isdecimal() == False:
        print("Web key must be a positive integer")
        web_key = input("Enter Web Key: ")
    data["webkey"] = web_key
    more_keys = True
    while more_keys:
        cur_key = input("Enter New Key: ")
        if len(cur_key) == 0:
            continue
        data[cur_key] = [int(x) for x in list(input(
            "Enter strip ids seperated by a , (no spaces): ").split(",")) if x.isdecimal()]
        more_keys = get_bool("Enter another key?")
    return data


def print_secondary_controller(i, folder, controller_data, keys, info):
    data = {
        "info": info,
        "keys": keys,
        "controllers": []
    }
    controller_data["primary"] = True
    data["controllers"].append(controller_data)
    config_file = open(folder + "/secondary_config_" + str(i) + ".json", "w")
    config_file.write(json.dumps(data))
    config_file.close()
    return


def create_new(file_name: str):
    print("Creating new config file with name:", file_name)
    data = {
        "info": {
            "date_generated": str(datetime.datetime.now()),
            "port": get_int("Enter port number: ", 80, 65535)
        }
    }
    data["keys"] = ask_keys()
    data["controllers"] = ask_controllers()
    config_file = open(file_name, "w")
    config_file.write(json.dumps(data))
    config_file.close()
    print("Config file generated:", file_name)
    folder_name = "secondary/" + file_name.split('.')[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    i = 1
    for controller in data["controllers"][1:]:
        print_secondary_controller(i, folder_name, controller, data["keys"], data["info"])
        i += 1
    print("Secondary controllers placed in", folder_name)
    print("To create folders for secondary controllers run ./secondary.py new", folder_name)


if len(sys.argv) < 2:
    print("Usage: ./gen_config.py <mode> [filename]")
    exit(1)

file_name = "config.json"
if len(sys.argv) == 3:
    file_name = sys.argv[2]

if file_name.split(".")[1] != "json":
    print("File must have .json extension")
    exit(1)

if sys.argv[1] == "new":
    create_new(file_name)
else:
    print("Usage: ./gen_config.py <mode> [filename]")
    print("Mode options are: new")
    exit(1)
