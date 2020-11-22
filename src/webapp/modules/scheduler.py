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

    def getSchedules(self):
        return self.config

    def getActiveSchedules(self):
        jobs = {}
        for s in self.schedules:
            jobs[s] = self.schedules[s].getJobs()
        return jobs

    def start(self, schedule_name: str, function_name: str):
        """Start schedule"""
        if schedule_name not in self.schedules:
            return False
        if not self.schedules[schedule_name].hasFunction(function_name):
            return False
        self.schedules[schedule_name].start(function_name)
        return True

    def stop(self, schedule_name: str, function_name: str):
        """Stops schedule"""
        if schedule_name not in self.schedules:
            return False
        if not self.schedules[schedule_name].hasFunction(function_name):
            return False
        return self.schedules[schedule_name].stop(function_name)

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
