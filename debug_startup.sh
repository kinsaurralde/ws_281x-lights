#!/bin/bash

cd "${0%/*}" # change directory to this files directory
cd app
sudo python3 -B app.py -td -c configs/localhost/main.yaml

