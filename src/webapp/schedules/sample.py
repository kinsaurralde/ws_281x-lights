from schedules.schedule_function_base import ScheduleFunctionBase

class ScheduleFunction(ScheduleFunctionBase):
    def __init__(self, scheduler, sequencer, config) -> None:
        super().__init__(scheduler, sequencer, config)

    def job_a(self):
        self.sequencer.run("sample", "blink", 1)

    def job_b(self):
        self.sequencer.run("sample", "test_e", None)

    def job_c(self):
        self.sequencer.stopAll()

    def test_a(self):
        self.add("test_a", self.s.every(.05).minutes.do(self.job_a))

    def test_b(self):
        self.add("test_b", self.s.every().day.at("20:34").do(self.job_b))

    def test_c(self):
        self.add("test_c", self.s.every().day.at("20:35").do(self.job_c))
