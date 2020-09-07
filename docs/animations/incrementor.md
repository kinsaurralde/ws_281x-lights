<!--- Function Links --->
[Color]: animations/animations.md#Color
[Pulse]: animations/animations.md#Pusle
[Wipe]: animations/animations.md#Wipe
[Rainbow]: animations/animations.md#Rainbow
[Cycle]: animations/animations.md#Cycle



<!--- Main Document --->

# Incrementors

The pixels class holds an ```IncrementArgs``` struct which is used by the increment functions. Increment functions
are not public and can only be set by an animation function and run by calling ```Pixels::increment()```.



## IncrementArgs

```cpp
typedef struct {
    unsigned int arg1;
    unsigned int arg2;
    unsigned int arg3;
    int arg4;
    int arg5;
    bool arg6;
    bool arg7;
    bool arg8;
    List* list;
} IncrementArgs;
```



## Functions

### Nothing
``void Pixels::nothing()``

Does nothing.

Used by: [Color][Color]



### Shifter
``void Pixels::shifter()``

Shifts pixels according to mode. If mode is blank, pixels brought in will be set to 0. If mode is
first_pixel, brought in pixel will be set to previous first pixel. If mode is loop, brought in pixel
will be set to the pixel that was pushed out the other side. Loop mode uses the list parameter which
allows the array being shifted to be larger than the number of pixels. This helps patterns be consistent
at the ends of the strip since number of LEDs isnt always divisible by the pattern length.

```cpp
IncrementArgs:
    arg1:           amount
    arg2:           mode                    (blank / first_pixel / loop) 
    arg6:           reverse                 (true / false)  
    list:           expanded pixels         (required for loop mode)
```

Used by: [Pulse][Pulse], [Wipe][Wipe], [Rainbow][Rainbow]



### Cycler
``void Pixels::cycler()``

Switches all pixels to next color in colors list.

```cpp
IncrementArgs:
    colors:         color list and counter
```

Used by: [Cycle][Cycle] 