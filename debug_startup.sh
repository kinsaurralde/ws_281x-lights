#!/bin/bash

cd "${0%/*}" # change directory to this files directory
cd app
sudo python3 app.py -t
