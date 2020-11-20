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

    
RED_GREEN_ALTERATE = {
    "colors": ["red", "green"],
    "length": 1,
    "spacing": 0,
    "wait_ms": 5000
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
        
