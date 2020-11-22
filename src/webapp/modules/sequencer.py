import importlib
import threading
import time


class Sequencer:
    """Handles running / stopping sequences"""

    def __init__(self, socketio, controller, config, colors):
        self.socketio = socketio
        self.controller = controller
        self.config = config
        self.colors = self._processColors(colors["colors"])
        self.sequences = {}
        self.active = {}
        self.thread_local = threading.local()
        self.thread_local.name = "Main"
        self._importSequences()

    def getSequences(self) -> dict:
        """Get sequence config"""
        return self.config

    def add(self, args: dict):
        """Send command to controllers"""
        self.controller.send([args])

    def checkActive(self, name: str) -> bool:
        """Checks if sequence name is running"""
        if name not in self.active:
            return False
        return self.active[name]["start_time"] == self.active[name]["saved_time"]

    def run(self, sequence_name: str, function_name: str, iterations: int = 1) -> bool:
        """Run sequence"""
        if sequence_name not in self.sequences:
            return False
        if not self.sequences[sequence_name].hasFunction(function_name):
            return False
        if iterations is not None:
            iterations = int(iterations)
        name = sequence_name + "-" + function_name
        start_time = time.time()
        thread = threading.Thread(target=self._sequenceRunThread, args=(name,))
        if name in self.active:
            print("FOUND")
            self.stop(sequence_name, function_name)
        self.active[name] = {
            "thread": thread,
            "start_time": start_time,
            "saved_time": start_time,
            "iterations": iterations,
            "sequence_name": sequence_name,
            "function_name": function_name,
        }
        thread.start()
        return True

    # def toggle(self, sequence_name, function_name, iterations=None):
    #     return False

    def stop(self, sequence_name: str, function_name: str) -> bool:
        """Stops sequence"""
        if sequence_name not in self.sequences:
            return False
        if not self.sequences[sequence_name].hasFunction(function_name):
            return False
        name = sequence_name + "-" + function_name
        if name not in self.active:
            return False
        self.active[name]["start_time"] = 0
        self.active[name]["thread"].join()
        self.active.pop(name)
        return True

    def stopAll(self):
        """Stops all running sequences"""
        for name in self.active:
            self.active[name]["start_time"] = 0
            self.active[name]["thread"].join()

    def _sequenceRunThread(self, name: str):
        if name not in self.active:
            return
        self.thread_local.name = name
        sequence_name = self.active[name]["sequence_name"]
        function_name = self.active[name]["function_name"]
        iterations = self.active[name]["iterations"]
        self.socketio.emit("start_sequence", {"name": name})
        try:
            while iterations is None or iterations > 0:
                self.sequences[sequence_name].run(function_name)
                if not self.checkActive(name):
                    break
                if iterations is not None:
                    iterations -= 1
        except:
            print("Exiting", self.thread_local.name)
        finally:
            self.socketio.emit("stop_sequence", {"name": name})

    def _importSequences(self):
        for s in self.config["sequences"]:
            if s["active"]:
                mod = importlib.import_module(s["module"])
                sequence = mod.Sequence(self, self.add, s)
                self.sequences[s["name"]] = sequence

    @staticmethod
    def _processColors(colors_config) -> dict:
        colors = {}
        for i, color in enumerate(colors_config["edit"]):
            colors[color["name"]] = colors_config["edit"][i]["value"]
        for i, color in enumerate(colors_config["noedit"]):
            colors[color["name"]] = colors_config["noedit"][i]["value"]
        return colors
