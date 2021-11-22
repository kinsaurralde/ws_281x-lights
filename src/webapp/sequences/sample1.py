import logging

from sequences.sequence_base import SequenceBase

log = logging.getLogger(__name__)
log.setLevel("DEBUG")

class Sequence(SequenceBase):
    def __init__(self) -> None:
        super().__init__()

    def a(self):
        log.info(f"Start sequence {self.name}-a")
        self.color(color="random")
