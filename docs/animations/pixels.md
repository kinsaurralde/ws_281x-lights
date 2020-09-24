# Pixels Class

The pixels class generates the frames of each animation. It does not set the actual LEDs. The
current animation is set by calling of the [animation functions](animations/animations.md#Functions) which
sets the first frame and the [incrementor function](animations/incrementor.md#Functions). The current frame
is returned from ```get()``` and the next frame is generated with ```increment()```.



## Animtaion Functions
Located [here](animations/animations.md#Functions)



## Public Functions

### Construtor
```Pixels::Pixels(unsigned int num_leds)```

Initialize Pixels Object.



### Get
``Frame* Pixels::get()``

Get a pointer to the current frame



### Increment
``void Pixels::increment()``

Generate next frame.



### Can Show
``bool Pixels::canShow(unsigned int ms = 0)``

Return true if enough time has passed to request next frame.



### Set Delay
``void Pixels::setDelay(unsigned int value)``

Set time inbetween frames.



### Set Size
``unsigned int Pixels::setSize(unsigned int size)``

Sets the number of LED pixels.



### Size
``unsigned int Pixels::size()``

Returns number of LED pixels.



### Get Brightness
``unsigned int Pixels::getBrightness()``

Returns current brightness



### Set Brightness
``void Pixels::setBrightness(unsigned int value)``

Sets brightness



### Set Increment Steps
``void Pixels::setIncrementSteps(unsigned int value = 1)``

Sets how many frames to jump when ```increment()``` is called.



### Initialize
``void Pixels::initialize(unsigned int num_leds, unsigned int milliwatts, unsigned int brightness, unsigned int max_brightness=255)``

Initialize strip with parameters



### Is Initialized
``bool Pixels::isInitialized()``

Retrun whether initialized or not