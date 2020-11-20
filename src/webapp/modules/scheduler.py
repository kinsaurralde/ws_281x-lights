import time
import threading
import importlib

import schedule


class Scheduler:
    """Create thread for scheduler to run"""

    def __init__(self, sequencer, config) -> None:
        self.sequencer = sequencer
        self.schedules = {}
        self.config = config
        self._importSchedules()
        self._start_thread()

    @staticmethod
    def _schedule_thread():
        while True:
            try:
                schedule.run_pending()
            except:
                print("Excpetion on scheduled task")
            time.sleep(1)

    def _importSchedules(self):
        for s in self.config["schedules"]:
            if s["active"]:
                mod = importlib.import_module(s["module"])
                sched = mod.ScheduleFunction(schedule, self.sequencer, s)
                self.schedules[s["name"]] = sched

    def _start_thread(self):
        thread = threading.Thread(target=self._schedule_thread)
        thread.setDaemon(True)
        thread.start()
