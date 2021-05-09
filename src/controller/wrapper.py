import ctypes
import os

LIB = ctypes.cdll.LoadLibrary(os.path.abspath("./pixels.so"))


class Frame(ctypes.Structure):
    _fields_ = [
        ("main", ctypes.c_uint * LIB.maxLEDPerStrip()),
        ("second", ctypes.c_uint * LIB.maxLEDPerStrip()),
    ]


class List(ctypes.Structure):
    def __init__(self, val):
        self.lib = LIB
        self.lib.List_new.argtypes = [ctypes.c_uint]
        self.lib.List_new.restype = ctypes.c_void_p
        self.lib.List_get.argtypes = [ctypes.c_uint, ctypes.c_uint]
        self.lib.List_get.restype = ctypes.c_uint
        self.lib.List_set.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
        self.lib.List_size.argtypes = [ctypes.c_void_p]
        self.lib.List_size.restype = ctypes.c_uint
        self.lib.List_setCounter.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        self.lib.List_getCounter.restype = ctypes.c_uint
        self.lib.List_getNext.restype = ctypes.c_uint
        self.lib.List_getCurrent.restype = ctypes.c_uint
        self.obj = self.lib.List_new(val)
        super().__init__()

    def get(self, index):
        return self.lib.List_get(self.obj, index)

    def set(self, index, value):
        self.lib.List_set(self.obj, index, value)

    def size(self):
        return self.lib.List_size(self.obj)

    def incrementCounter(self):
        self.lib.List_incrementCounter(self.obj)

    def decrementConter(self):
        self.lib.List_decrementCounter(self.obj)

    def setCounter(self, value):
        self.lib.List_setCounter(self.obj, value)

    def getCounter(self):
        return self.lib.List_getCounter(self.obj)

    def getNext(self):
        return self.lib.List_getNext(self.obj)

    def getCurrent(self):
        return self.lib.List_getCurrent(self.obj)


MAX_BRIGHTNESS = 127

class Pixels:
    def __init__(self, val):
        self.lib = LIB
        self.lib.Pixels_new.argtypes = [ctypes.c_uint]
        self.lib.Pixels_new.restype = ctypes.c_void_p
        self.lib.Pixels_canShow.argtypes = [ctypes.c_uint, ctypes.c_uint]
        self.lib.Pixels_canShow.restype = ctypes.c_bool
        self.lib.Pixels_setDelay.argtypes = [ctypes.c_uint, ctypes.c_uint]
        self.lib.Pixels_getDelay.argtypes = [ctypes.c_void_p]
        self.lib.Pixels_getDelay.restype = ctypes.c_uint
        self.lib.Pixels_setSize.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        self.lib.Pixels_size.restype = ctypes.c_uint
        self.lib.Pixels_getBrightness.restype = ctypes.c_uint
        self.lib.Pixels_setBrightness.argtypes = [ctypes.c_uint, ctypes.c_uint]
        self.lib.Pixels_setIncrementSteps.argtypes = [ctypes.c_uint, ctypes.c_uint]
        self.lib.Pixels_initialize.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool]
        self.lib.Pixels_isInitialized.argtypes = [ctypes.c_void_p]
        self.lib.Pixels_isInitialized.restype = ctypes.c_bool
        self.lib.Pixels_isGRB.argtypes = [ctypes.c_void_p]
        self.lib.Pixels_isGRB.restype = ctypes.c_bool
        self.lib.Pixels_get.restype = ctypes.POINTER(Frame)
        self.lib.Pixels_animation.argtypes = [ctypes.c_uint, ctypes.c_void_p]
        self.lib.createAnimationArgs.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, ctypes.c_bool]
        self.lib.createAnimationArgs.restype = ctypes.c_void_p
        self.lib.Pixels_getCurrentState.argtypes = [ctypes.c_void_p]
        self.lib.Pixels_getCurrentState.restype = ctypes.c_long
        self.obj = self.lib.Pixels_new(val, MAX_BRIGHTNESS)

    def canShow(self, ms):
        return self.lib.Pixels_canShow(self.obj, ms)

    def setDelay(self, value):
        self.lib.Pixels_setDelay(self.obj, value)

    def getDelay(self):
        return self.lib.Pixels_getDelay(self.obj)

    def setSize(self, value):
        self.lib.Pixels_setSize(self.obj, value)

    def size(self):
        return self.lib.Pixels_size(self.obj)

    def getBrightness(self):
        return self.lib.Pixels_getBrightness(self.obj)

    def setBrightness(self, value):
        self.lib.Pixels_setBrightness(self.obj, value)

    def setIncrementSteps(self, value):
        self.lib.Pixels_setIncrementSteps(self.obj, value)

    def initialize(self, num_leds, milliwatts, brightness, max_brightness, grb):
        self.lib.Pixels_initialize(self.obj, num_leds, milliwatts, brightness, max_brightness, grb)

    def isInitialized(self):
        return self.lib.Pixels_isInitialized(self.obj)

    def isGRB(self):
        return self.lib.Pixels_isGRB(self.obj)

    def get(self):
        return self.lib.Pixels_get(self.obj)

    def increment(self):
        self.lib.Pixels_increment(self.obj)

    def animation(self, args):
        args_pointer = self.lib.createAnimationArgs(args.animation, args.color, args.color_bg, args.colors.obj, args.wait_ms, args.arg1, args.arg2, args.arg3, args.arg4, args.arg5, args.arg6, args.arg7, args.arg8)
        self.lib.Pixels_animation(self.obj, args_pointer)

    def getCurrentState(self):
        state_pointer = self.lib.Pixels_getCurrentState()


class AnimationArgs:
    def __init__(self):
        self.animation = 0
        self.color = 0
        self.color_bg = 0
        self.colors = List(0)
        self.wait_ms = 0
        self.arg1 = 0
        self.arg2 = 0
        self.arg3 = 0
        self.arg4 = 0
        self.arg5 = 0
        self.arg6 = False
        self.arg7 = False
        self.arg8 = False
