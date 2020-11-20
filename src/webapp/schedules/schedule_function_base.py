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
        self._setup_schedules()

    def _createFunctionTable(self):
        for function in self.functions_config:
            try:
                self.function_table[function] = getattr(self, function)
            except AttributeError:
                print(f"Function {function} for schedule {self.name} does not exist!")

    def _setup_schedules(self):
        for function in self.function_table:
            if self.functions_config[function]["active"]:
                self.function_table[function]()
