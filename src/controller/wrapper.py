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
        self.lib.Pixels_color.argtypes = [ctypes.c_uint, AnimationArgs]
        self.lib.Pixels_wipe.argtypes = [ctypes.c_uint, AnimationArgs]
        self.lib.Pixels_pulse.argtypes = [ctypes.c_uint, AnimationArgs]
        self.lib.Pixels_rainbow.argtypes = [ctypes.c_uint, AnimationArgs]
        self.lib.Pixels_cycle.argtypes = [ctypes.c_uint, AnimationArgs]
        self.obj = self.lib.Pixels_new(val, MAX_BRIGHTNESS)

    def canShow(self, ms):
        return self.lib.Pixels_canShow(self.obj, ms)

    def setDelay(self, value):
        self.lib.Pixels_setDelay(self.obj, value)

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

    def color(self, args):
        self.lib.Pixels_color(self.obj, args)

    def wipe(self, args):
        self.lib.Pixels_wipe(self.obj, args)

    def pulse(self, args):
        self.lib.Pixels_pulse(self.obj, args)

    def rainbow(self, args):
        self.lib.Pixels_rainbow(self.obj, args)

    def cycle(self, args):
        self.lib.Pixels_cycle(self.obj, args)


class AnimationArgs(ctypes.Structure):
    _fields_ = [
        ("animation", ctypes.c_uint),
        ("color", ctypes.c_int),
        ("color_bg", ctypes.c_int),
        ("colors", ctypes.c_void_p),
        ("wait_ms", ctypes.c_uint),
        ("arg1", ctypes.c_uint),
        ("arg2", ctypes.c_uint),
        ("arg3", ctypes.c_uint),
        ("arg4", ctypes.c_int),
        ("arg5", ctypes.c_int),
        ("arg6", ctypes.c_bool),
        ("arg7", ctypes.c_bool),
        ("arg8", ctypes.c_bool),
    ]
