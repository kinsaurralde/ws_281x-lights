# Lights
This project contains a flask webserver that provides a website to control rgb lights through the rpi_ws281x library.
___

## Web API Routes
  
  Params are seperated by a ','
  
#### Index: '/'
* Main control page

#### Off: '/off'
* Stop animations and turn all pixels off

#### Stop Animation: '/stopanimation'
* Stops all animations

#### Get Data: '/get'
* Get data on current settings and pixel colors

#### Get Docs: '/docs'
* Get this document in html form

#### Reverse: '/reverse'
* Flip strip

#### Settings: '/settings/\<param>'
* Change settings
* given setting_name=value
* Functions:
    * "break": change break_animation value
    * "brightness": change brightness

#### Operations: '/operations/\<function>/\<param>'
* One time pixel changes
* Functions:
    * "shift": shift pixels by amount
        * Params:
            1. amount: amount to pixels to shift by
            2. post_delay: amount of pixels to wait after shifting
    * "reverse": Flip strip

#### Run: '/run/\<function>/\<param>'
* Non repeating actions
* Functions:
    * "color": set all lights to same color
        * Params:
            1. r value
            2. g value
            3. b value
    * "wipe": wipe a color across the strip
        * Params:
            1. r value
            2. g value
            3. b value
            4. direction
                * 1: forward direction
                * -1: reverse direction
            5. wait_ms: how long before moving to next pixel (in ms)
    * "single": set a single pixel to a color
        * Params:
            1. pixel id: which pixel to set
            2. r value
            3. g value
            4. b value
    * "pulse": move a pulse of color across strip
        * Params:
            1. r value
            2. g value
            3. b value
            4. direction
                * 1: forward direction
                * -1: reverse direction
            5. wait_ms: how long before moving to next pixel (in ms)
            6. length: how many pixels in pulse
    * "specific": set specific pixels to same color
        * Params:
            * One param per pixel to set
            * Each pixel has following data seperated by a '.'
                1. pixel id:
                2. r value
                3. g value
                4. b value


#### Animate: '/animate/\<function>/\<param>'
* Repeating actions
* Will stop any previous animations
* Functions:
    * "chase": movie theater light style chaser animation
        * Params:
            1. r value
            2. g value
            3. b value
            4. wait_ms: delay between pixel changes (in ms)
    * "rainbowCycle": draw rainbow that uniformly distributes itself across all pixels
        * Params:
            1. wait_ms: delay between pixel changes (in ms)
    * "rainbowChase": rainbow movie theater light style chaser animation
        * Params:
            1. wait_ms: delay between pixel changes (in ms)
    * "randomCycle": change to random colors
        * Params:
            1. each
                * "true": each pixel picks a random color seperatly
                * else: entire strip switch to same random color
            2. wait_ms: delay between color changes (in ms)
    * "shift": shift each pixel by an amount
        * Params:
            1. amount: number of pixels to shift by each frame
            2. wait_ms: delay between shifts (in ms)
    * "pulse": move a pulse of color across strip
        * Params:
            1. r value
            2. g value
            3. b value
            4. direction
                * 1: forward direction
                * else: reverse direction
            5. wait_ms: how long before moving to next pixel (in ms)
            6. length: number of pixels in pulse
    * "mix": switch between multiple colors
        * Params:
            1. wait_ms: delay between given color changes
                * <0: instantly switch between given color changes after |wait_ms| ms
                * else: mix between colors with wait_ms between full given colors
            2. colors: array of colors to switch between
                * colors seperated by a ','
                * r, g, b values seperated by a '.'
