import importlib
import threading
import time


class Sequencer:
    def __init__(self, socketio, controller, config):
        self.socketio = socketio
        self.controller = controller
        self.config = config
        self.sequences = {}
        self.active = {}
        self.thread_local = threading.local()
        self.thread_local.name = "Main"
        self._importSequences()

    def _importSequences(self):
        for s in self.config["sequences"]:
            if s["active"]:
                mod = importlib.import_module(s["module"])
                sequence = mod.Sequence(self, self.add, s)
                self.sequences[s["name"]] = sequence
        print(self.config)

    def getSequences(self):
        return self.config

    def add(self, args):
        print("SENDING", args)
        self.controller.send([args])

    def _sequenceRunThread(self, name):
        if name not in self.active:
            return
        self.thread_local.name = name
        sequence_name = self.active[name]["sequence_name"]
        function_name = self.active[name]["function_name"]
        iterations = self.active[name]["iterations"]
        self.socketio.emit("start_sequence", {"name": name})
        while iterations is None or iterations > 0:
            self.sequences[sequence_name].run(function_name)
            if not self.checkActive(name):
                break
            iterations -= 1
        self.socketio.emit("stop_sequence", {"name": name})

    def checkActive(self, name):
        if name not in self.active:
            return False
        return self.active[name]["start_time"] == self.active[name]["saved_time"]

    def run(self, sequence_name, function_name, iterations=3):
        if sequence_name not in self.sequences:
            return
        if not self.sequences[sequence_name].hasFunction(function_name):
            return
        name = sequence_name + "-" + function_name
        start_time = time.time()
        thread = threading.Thread(target=self._sequenceRunThread, args=(name,))
        self.active[name] = {
            "thread": thread,
            "start_time": start_time,
            "saved_time": start_time,
            "iterations": iterations,
            "sequence_name": sequence_name,
            "function_name": function_name,
        }
        thread.start()

    def toggle(self, sequence_name, function_name, iterations=None):
        pass

    def stop(self, sequence_name, function_name):
        if sequence_name not in self.sequences:
            return
        if not self.sequences[sequence_name].hasFunction(function_name):
            return
        name = sequence_name + "-" + function_name
        if name not in self.active:
            return
        self.active[name]["start_time"] = 0

    def stopAll(self):
        for name in self.active:
            self.active[name]["start_time"] = 0
