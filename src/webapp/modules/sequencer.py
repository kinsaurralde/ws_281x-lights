import logging
import importlib

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class Sequencer:
    def __init__(self, modules, config) -> None:
        self._setupSequences(config["sequences"])
        self.sequences = {}
        self.modules = modules

    def _setupSequences(self, sequences):
        self.sequences = sequences
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
