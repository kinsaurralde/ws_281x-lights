import importlib


class Sequencer:
    def __init__(self, controller, config):
        self.controller = controller
        self.config = config
        self.sequences = {}
        self._importSequences()

    def _importSequences(self):
        for s in self.config["sequences"]:
            if s["active"]:
                mod = importlib.import_module(s["module"])
                sequence = mod.Sequence(self.add, s)
                self.sequences[s["name"]] = sequence
                print(sequence)

    def add(self, args):
        print("SENDING", args)
        self.controller.send([args])

    def run(self, sequence_name, function_name):
        if sequence_name in self.sequences:
            self.sequences[sequence_name].run(function_name)
