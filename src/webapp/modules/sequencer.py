import logging
import importlib

import config

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class Sequencer:
    def __init__(self, globals, config) -> None:
        self._setupSequences(config["sequences"])
        self.sequences = {}
        self.globals = globals

    def _setupSequences(self, config):
        self.sequences = config
        for name, values in self.sequences.items():
            if "module" not in values or "functions" not in values:
                log.warning(f"Sequence {name} missing module")
                continue
            module_path = values["module"]
            functions = values["functions"]
            print(f"{name}: {module_path} {functions}")
            try:
                mod = importlib.import_module(module_path)
                sequence = mod.Sequence()
                sequence.setup(name, functions)
            except ModuleNotFoundError:
                log.error(f"Sequence {name} cannout find module {module_path}")
