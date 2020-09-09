# ws281x-led

Full documentation [here](https://kinsaurralde.github.io/ws_281x-lights/#/)

## Table of Contents
1. [Top Level Directory Structure](#top-level-directory-structure)
2. [Installation](#installation)
3. [Building](#building)
4. [Testing](#testing)
5. [Tools](#tools)
6. [Application Architecture](#application-architecture)
7. [TODO](#todo)

## Top Level Directory Structure
```
.
├── build
├── docs                # Documentation files
├── images              # Images used for README or other docs
├── lint_config         # Configuration for linters
├── src                 # Source files
├── tools               # Programs used to copy, send, or test
├── makefiles           # Makefiles for raspberrypi
├── .gitignore
├── Makefile
├── LICENSE
└── README.md
```

## Installation
1. Install python3 and make if not already installed

2. Clone this repository using
```bash
git clone https://github.com/kinsaurralde/ws_281x-lights
```

3. Run
```bash
make setup
```
to install dependencies

## Building
Running
```bash
make
```
will copy files to the build directory.
The subdirectories of the build directory can be copied or sent to the devices they will actually run on.

```
.
├── ...
├── build
│   ├── esp8266             # Webserver for esp8266 and source files for pixels shared object
│   ├── raspberrypi         # Flask Webserver for raspberry pi and source files for pixels shared object
│   └── webapp              # Flask Webserver for webapp
└── ...
```

The esp8266 directory can be directly uploaded to an esp8266 connected over serial.
It is easiest to do this in the Arduino IDE as its library manager is needed to download libraries.
The files in this directory are only intended for an esp8266.


The raspberrypi directory can be put on a raspberry pi by manually copying or by using the upload_rpi tool.
Once on the raspberry pi, it can be build by running `make setup` if necessary then `make`.
The files in this directory are only intended for a raspberry pi.

The webapp directory can be run on any device that has python since it does not interact with special hardware that the esp8266 and raspberry pi use.

## Testing
Tests can be run through either
```bash
make test
```
for all tests with coverage report OR
```bash
make test_webapp
```
to just test the webapp server with no coverage report.

Currently only the webapp server has tests.

A coverage report in HTML format is available at `src/webapp/htmlcov/index.html`

## Tools

```
.
├── ...
├── tools
│   ├── configs
|   |   ├── localtest.yaml
|   |   └── upload_rpi.yaml 
│   ├── localtest.py
│   └── upload_rpi.py
└── ...
```

### localtest
Localtest creates locally test controler servers. It uses the controller config specified in `localtest.yaml`. 
The controller servers run in test mode with incrementing port numbers starting at 6000.

Arguments:
```
usage: localtest.py [-h] [-c CONFIG] [-b BUILDFOLDER]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config file
  -b BUILDFOLDER, --buildfolder BUILDFOLDER
                        Path to buildfolder
```

This can be run by either
```bash
cd tools
./localtest.py
```
or
```bash
make run_local
```

### upload_rpi
Upload rpi uses sftp to send the required files to other devices (most likely raspberry pis).
The locations to send through and other information can be set in `upload_rpi.yaml`

Arguments:
```
usage: upload_rpi.py [-h] [-c CONFIG] [-b BUILDFOLDER]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config file
  -b BUILDFOLDER, --buildfolder BUILDFOLDER
                        Path to buildfolder
```

This can be run by either
```bash
cd tools
./upload_rpi.py
```
or
```bash
make upload_rpi
```

Config file example (default value)
```
- userhost: pi@rpi4.kinsaurralde.com      # user@hostname
  key: "~/.ssh/rpi4"                      # path to ssh key
  destination: "Files/test_rgb/"          # folder that files should be put into
  webapp: false                           # include webapp compenent
  controller: true                        # include controller component
```


## Application Architecture
![Application Architecture](images/application_architecture.png)

## Todo
- Controller brightness
- Power consumption measurement and adjustment
- SocketIO
    - Controller ping on webpage
    - Controller brighntess on webpage
    - Controller connected on webpage
    - Webapp expected pixel colors
- Add webapp to upload_rpi.py
- Hide/Show sections on webpage
- Tests for controllers
- Verion numbers
- Update README
