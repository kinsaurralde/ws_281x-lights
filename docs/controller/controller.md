# Controller

The controller recieves commands from the webserver, generates animations, and sends signals to the LED strip. 
The ESP8266 version uses the [FastLED library](https://github.com/FastLED/FastLED) while
the Raspberry Pi version uses the [rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python).
Both versions implement the routes below and have the same behavior. 
The ESP8266 version has special routes [here](#esp8266-special-routes).

## Animation Type
The animation type property is sent using an unsigned int. The animation that corresponds to each value
is listed below.
```cpp
enum Animation {
    color,          // 0
    wipe,           // 1
    pulse,          // 2
    rainbow,        // 3
    cycle           // 4
};
```

## Routes
The ESP8266 version is called through a webserver. The web routes are listed below along with request type,
arguments, and return type.

### /data
**POST**

JSON payload is an array of objects with the following properties. All properties should be included in each 
request although defaults will be used if a property is not present.

| Property      | Type                      | Description
|---------------|---------------------------|------------------------
| id            | unsigned int              | which LED strip
| inc_steps     | unsigned int              | how many times incremented per next frame
| animation     | Animation (unsigned int)  | which animation to use
| color         | int                       | single color to use
| color_bg      | int                       | typicaly a background color
| colors        | List (unsigned int)       | list of colors
| wait_ms       | unsigned int              | time between frames
| arg1          | unsigned int              | AnimationArg
| arg2          | unsigned int              | AnimationArg
| arg3          | unsigned int              | AnimationArg
| arg4          | int                       | AnimationArg
| arg5          | int                       | AnimationArg
| arg6          | bool                      | AnimationArg
| arg7          | bool                      | AnimationArg
| arg8          | bool                      | AnimationArg

Return: empty list (will probably change)

### /init
**POST**

Initializes pixels with led_count, brightness, and maximum milliwatts

| Property          | Type                      | Description
|-------------------|---------------------------|------------------------
| id                | unsigned int              | which LED strip
| init              | JSON Object               | init values
| init.num_leds     | unsigned int              | number of pixels 
| init.milliwatts   | unsigned int              | maximum power in milliwatts
| init.brightness   | unsigned int              | starting brightness

Return: text (will probably change)

### /getpixels
**GET**

Gets current color of both strip's pixels. 

Return: 2D array

### /brightness
**GET**

Sets brightness if query param value present. Then return current brightness.

Query Params:
* id:       which LED strip
* value:    new brightness

Return: int

## ESP8266 Special Routes
These special routes deal with ESP8266 hardware. 
They exists on other controller types but only return some insignificant value.

### /heapfree
**GET**

Gets amount of heap bytes that are currently free.

Return: int

## /ledon
**GET**

Turns the built in LED on

Return: text

## /ledoff
**GET**

Turns the build in LED off

Return: text