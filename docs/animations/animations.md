<!--- Incrementor Links --->
[Nothing]: animations/incrementor.md#Nothing
[Shifter]: animations/incrementor.md#Shifter
[Cycler]: animations/incrementor.md#Cycler



<!--- Main Document --->

# Animations

All animation functions take an ```AnimationArgs``` struct as a parameter and have a return type of ```void```.
Animation fuctions set the starting frame and an [incrementor](animations/incrementor.md) that handles the animation.
Animation functions should be called by the controller file, [```controller.ino```](controller/) for an esp8266, 
and [```controller.py```](controller/) for a raspberry pi.



## AnimationArgs
```cpp
typedef struct {
    Animation animation;
    int color;
    int color_bg;
    List* colors;
    unsigned int wait_ms;
    unsigned int arg1;
    unsigned int arg2;
    unsigned int arg3;
    int arg4;
    int arg5;
    bool arg6;
    bool arg7;
    bool arg8;
} AnimationArgs;
```



## Functions

### Color
``void Pixels::color(AnimationArgs args)``

Set entire LED strip to color.

```cpp
AnimationArgs:
    color:          color
```

Incrementor: [Nothing][Nothing]



### Pulse
``void Pixels::pulse(AnimationArgs args)``

Draw patten on LED strip then shift. For each color in colors, arg1 pixels are set to that color followed
by arg2 pixels set to color_bg. If background color < 0, it is ignored and background pixels will keep 
their previous color. However, the shifter animation will move all pixels, including background ones.

```cpp
AnimationArgs:
    colors:         list of pulse colors
    color_bg:       background color
    arg1:           length
    arg2:           spacing length
    arg3:           shifter amount
    arg4:           expanded size           ( < num_leds if not used)
    arg6:           reverse                 (true / false)
```

Incrementor: [Shifter][Shifter]



### Wipe
``void Pixels::wipe(AnimationArgs args)``

Makes all pixels become color sequentially. Before starting, all pixels are set to color_bg unless it is < 0.

```cpp
AnimationArgs:
    color:          wipe color
    color_bg:       background color
    arg1:           steps
    arg6:           reverse
```

Incrementor: [Shifter][Shifter]



### Rainbow
``void Pixels::rainbow(AnimationArgs args)``

Sets pixels to rainbow pattern.

```cpp
AnimationArgs:
    arg3:           shifter amount
    arg6:           reverse                 (true / false)     
```

Incrementor: [Shifter][Shifter]



### Cycle
``void Pixels::cycle(AnimationArgs args)``

Switches all pixels between given colors. If arg1 == 1, then next color in colors list will be set 
everytime incrementor is called. If arg1 > 1, adjacent colors in colors list are blended together.

```cpp
AnimationArgs:
    colors:         list of colors to cycler
    arg1:           steps between colors
```

Incrementor: [Cycler][Cycler]

### randomCycle
``void Pixels::randomCycle(AnimationArgs args)``

Switches all pixels between random colors.

```cpp
AnimationArgs:
    arg1:           seed for random number generator
```

Incrementor: [Cycler][Cycler]

### Reverser
``void Pixels::reverser(AnimationArgs args)``

Reverse increment direction, pixels positions, or both

```cpp
AnimationArgs:
    arg6:           reverse incrementor     (true / false)
    arg7:           reverse pixels          (true / false)
```

Incrementor: Does not change current incrementor
