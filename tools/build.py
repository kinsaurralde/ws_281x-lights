#!/usr/bin/env python3

import argparse
import datetime
import shutil
import yaml


parser = argparse.ArgumentParser(
    description="Copy source files to build directory")
parser.add_argument("--webapp-output-dir", default="../build/webapp/",
                    help="Directory to output webapp")
parser.add_argument("--esp-output-dir", default="../build/esp/",
                    help="Directory to output esp controller")
parser.add_argument("--webapp-src-dir", default="../src/webapp")
parser.add_argument("--esp-src-dir", default="../src/controller")

args = parser.parse_args()

timestamp = datetime.datetime.now()

def openYaml(path):
    """Open yaml file and return as a dictionary"""
    data = {}
    with open(path) as open_file:
        data = yaml.safe_load(open_file)
    return data

def openYamlBackup(path, backup_path="config/example.build.yaml"):
    try:
        return openYaml(path)
    except FileNotFoundError:
        return openYaml(backup_path)

config_data = openYamlBackup("config/build.yaml")

shutil.copytree(args.webapp_src_dir, args.webapp_output_dir)
shutil.copytree(args.esp_src_dir, args.esp_output_dir)

with open(f'{args.esp_output_dir}wifi_credentials.h', 'w') as file:
    file.write(f"#define WIFI_SSID \"{config_data['wifi']['ssid']}\"\n")
    file.write(f"#define WIFI_PASSWORD \"{config_data['wifi']['password']}\"\n")
