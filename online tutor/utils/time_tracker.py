# utils/time_tracker.py
import time
from config import ABSENCE_TIME_LIMIT

class AbsenceTimer:
    def __init__(self):
        self.start_time = None

    def update(self, absent):
        if absent:
            if self.start_time is None:
                self.start_time = time.time()
        else:
            self.start_time = None

    def exceeded_limit(self):
        if self.start_time is None:
            return False
        return time.time() - self.start_time > ABSENCE_TIME_LIMIT
