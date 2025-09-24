import math

REWARDS_HEADER = "Rewards"
METRICS_HEADER = "Metrics"

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


def nest_dict(flat_dict, total_first=True):
    nested = {}
    for flat_key, value in flat_dict.items():
        parts = flat_key.split("/")
        current = nested
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                old_val = current[part]
                current[part] = {}
                if total_first:
                    current[part]["Total"] = old_val
                else:
                    current[part] = {**current[part], "Total": old_val}
            current = current[part]
        last = parts[-1]
        if last in current and isinstance(current[last], dict):
            if total_first:
                # Move 'Total' to first if exists, else insert
                if "Total" not in current[last]:
                    current[last] = {"Total": value, **current[last]}
                else:
                    current[last]["Total"] = value
            else:
                current[last]["Total"] = value
        elif last in current and not isinstance(current[last], dict):
            old_val = current[last]
            current[last] = {}
            if total_first:
                current[last]["Total"] = old_val
                current[last]["Total"] = value
            else:
                current[last] = {**current[last], "Total": value}
        else:
            current[last] = value
    return nested