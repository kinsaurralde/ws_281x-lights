import logging

log = logging.getLogger(__name__)
log.setLevel("DEBUG")

class ScheduleFunctionBase:
    def __init__(self, scheduler, sequencer, config):
        self.scheduler = scheduler
        self.s = self.scheduler
        self.sequencer = sequencer
        self.functions_config = config["functions"]
        self.name = config["name"]
        self.jobs = {}
        self.function_table = {}
        self._createFunctionTable()
        self.start_all(config["active"])

    def _createFunctionTable(self):
        for function in self.functions_config:
            try:
                self.function_table[function] = getattr(self, function)
            except AttributeError:
                log.info(f"Function {function} for schedule {self.name} does not exist!")

    def hasFunction(self, name):
        return name in self.function_table

    def start_all(self, active=True):
        if not active:
            return False
        for function in self.function_table:
            self.start(function)
        return True

    def start(self, function):
        if function not in self.jobs:
            self.function_table[function]()

    def stop(self, function):
        if function not in self.jobs:
            return False
        self.scheduler.cancel_job(self.jobs[function])
        self.jobs.pop(function)
        return True

    def add(self, name, job):
        self.jobs[name] = job

    def getJobs(self):
        return list(self.jobs.keys())
