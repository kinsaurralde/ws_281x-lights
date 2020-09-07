#!/bin/bash

cd "${0%/*}" # change directory to this files directory
sudo screen -dmS rgb_server sudo python3 controller_server.py "$@"
