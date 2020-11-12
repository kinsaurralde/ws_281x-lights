import time

from sequences.sequence_base import SequenceBase

class Sequence(SequenceBase):
    def __init__(self, sequencer, send, config) -> None:
        super().__init__(sequencer, send, config)
        self.presetArgs()

    def presetArgs(self):
        self.controller_presets = {
            'tester_a_0': self.createControllerArgs(strip_id='tester_a_0')
        }

        self.animation_presets = {
            'color_blue': {
                'color': 255
            },
            'wipe_green': {
                'color': 65280
            }
        }

    def test_a(self):
        self.color(**self.animation_presets['color_blue'], controller_args=self.controller_presets['tester_a_0'])

    def test_b(self):
        self.wipe(**self.animation_presets['wipe_green'], controller_args=self.controller_presets['tester_a_0'])
        self.sleep(8)
        self.color(**self.animation_presets['color_blue'], controller_args=self.controller_presets['tester_a_0'])
        self.sleep(2)
