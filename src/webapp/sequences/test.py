import time

from sequences.sequence_base import SequenceBase, Preset

class Sequence(SequenceBase):
    def __init__(self, sequencer, send, config) -> None:
        super().__init__(sequencer, send, config)

    def test_a(self):
        self.pulse()

    def test_b(self):
        self.wipe(**Preset['wipe_green'])
        self.sleep(4)
        self.wipe(**Preset['wipe_green_r'])
        self.sleep(4)
        self.color(**Preset['color_blue'])
        self.sleep(2)
        
