# ws_281x-lights

This project contains a flask webserver that provides a website to control rgb lights through the rpi_ws281x library.

## Installation

Clone this repository then run
```bash
./setup.sh
```

## Usage

Plugin LED strip with data on GPIO pin 18

Guide at: https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring

To create config file:
```bash
cd tools
./gen_config.py new [filename]
```

If there are secondary controllers
```bash
./secondary.py new [foldername]
./put_files.py [sftp_path]
```

Run
```bash
./startup.sh [config_file]
```

On remote controllers
```bash
./startup.sh
```

## Flask Server (app.py)

* Receives requests to web routes, checks keys, and passes information to multicontroller (multicontroller.py)
* Returns JSON message with strip and error status
* multicontroller.py
    * Forward requests to local or remote controller
* controller.py
    * Calls given function with their arguments
    * Creates virtual strips and passes their information to neopixel class (lights.py)
* lights.py
    * Lights class contains functions that change specific LED colors according to pattern
    * Neopixels class adjusts pixel ids for virtual strips and sends to rpi_ws281x library to change 
      physical LED strip


## Main Web Page

* Creates a url based on input boxes
* Sends commands to flask server though url

## Keys Web Page

* View/Change Keys and which light strips they can access

## Info Web Page

* View current settings
* View controllers and their virtual strips
* View current color of all LEDs on all strips

## Tools

* Config file generator
* Send json to url
* Update secondary controller files
* Upload secondary controller files to another raspberry pi

[More Information](tools/README.md)


## License
[MIT](https://choosealicense.com/licenses/mit/)
