from sequences.sequence_base import SequenceBase

class Sequence(SequenceBase):
    def __init__(self, sequencer, send, config) -> None:
        super().__init__(sequencer, send, config)

    def basic(self):
        self.pulse("a", **RED_GREEN_ALTERATE)
        self.pulse("c", **WHITE_BLUE_ALTERNATE)
        self.sleep(10)
        self.pulse("c", **WHITE_BLUE_ALTERNATE_R)
        self.sleep(10)

    def home(self):
        self.pulse(**RED_GREEN_ALTERATE)
        self.sleep(5)
        self.pulse(**RED_GREEN_ALTERATE_R)
        self.sleep(5)
        self.rainbow()
        self.sleep(3)
        self.sequencer.run("sample", "blink", 8)
        self.sleep(10)
        self.color(color="red")
        self.wipe(color="green")
        self.sleep(10)
        self.cycle()
        self.sleep(10)
        self.pulse(**PULSE)
        self.sleep(10)

    def new(self):
        self.randomCycle(wait_ms=400)
        self.sleep(12)
        max_seconds = 3
        self.pulse(**RED_GREEN_ALTERATE)
        for i in range(max_seconds):
            self.sleep(max_seconds - i)
            self.reverser(reverse_animation=True, reverse_pixels=False)
            self.sleep(max_seconds - i)
            self.reverser(reverse_animation=True, reverse_pixels=False)
        self.rainbow(steps=5)
        self.sleep(12)
        for _ in range(6):
            self.wipe(steps=12, color="green", reverse=False)
            self.sleep(1)
            self.wipe(steps=12, color="red", reverse=True)
            self.sleep(1)
        self.cycle(steps=6)
        self.sleep(12)



    
RED_GREEN_ALTERATE = {
    "colors": ["red", "green"],
    "length": 15,
    "spacing": 0,
    "wait_ms": 50,
    "reverse": False
}

RED_GREEN_ALTERATE_R = {
    "colors": ["red", "green"],
    "length": 15,
    "spacing": 0,
    "wait_ms": 50,
    "reverse": True
}

WHITE_BLUE_ALTERNATE = {
    "colors": ["blue", "white"],
    "length": 15,
    "spacing": 0,
    "wait_ms": 75,
    "reverse": False
}

WHITE_BLUE_ALTERNATE_R = {
    "colors": ["blue", "white"],
    "length": 15,
    "spacing": 0,
    "wait_ms": 75,
    "reverse": True
}

PULSE = {
    "colors": ["red", "turquoise", "green", "purple", "blue", "pink"],
    "length": 10,
    "spacing": 10,
    "wait_ms": 60
}      
