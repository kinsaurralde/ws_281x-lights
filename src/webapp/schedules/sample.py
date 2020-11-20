from schedules.schedule_function_base import ScheduleFunctionBase

class ScheduleFunction(ScheduleFunctionBase):
    def __init__(self, scheduler, sequencer, config) -> None:
        super().__init__(scheduler, sequencer, config)

    def job_a(self):
        print("START A")

    def job_b(self):
        print("START B")
        self.sequencer.run("sample", "test_e", None)

    def job_c(self):
        print("STOP")
        self.sequencer.stopAll()

    def test_a(self):
        return self.s.every(.1).minutes.do(self.job_a)

    def test_b(self):
        return self.s.every().day.at("20:34").do(self.job_b)

    def test_c(self):
        return self.s.every().day.at("20:35").do(self.job_c)
