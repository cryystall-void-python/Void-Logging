import math

REWARDS_HEADER = "Rewards"
METRICS_HEADER = "Metrics/"

class AvgTracker:
    def __init__(self):
        self._value = 0
        self._count = 0

    def __iadd__(self, other):
        self._value += other
        self._count += 1

        return self

    def get_avg(self):
        if self._count == 0:
            return math.nan
        return self._value / self._count
