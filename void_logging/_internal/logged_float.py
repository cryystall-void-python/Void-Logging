import warnings

from .._internal.stat import Stat
from ..api.rewards import Log


class LoggedFloat:
    def __init__(self, metrics: list[str] = None):
        if metrics is None:
            self.metrics = []
        else:
            self.metrics = metrics

        self.logs: dict[str, Stat] = {}
        self.value = 0

        self.init_metrics()

    def __del__(self):
        self.logs.clear()
        self.metrics.clear()

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_log_value(self, log_name: str):
        return self.logs.get(log_name).value

    def __iadd__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.value += other[0]
        if other[1] not in self.logs.keys():
            self.logs.setdefault(other[1], Stat())
            self.metrics.append(other[1])

        self.logs[other[1]] += other[0]
        return self

    def __isub__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.value -= other[0]
        if other[1] not in self.logs.keys():
            self.logs.setdefault(other[1], Stat())
            self.metrics.append(other[1])

        self.logs[other[1]] -= other[0]
        return self

    def __imul__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        diff = (other[0] - 1) * self.value
        return self.__iadd__(Log(diff, other[1]))

    def __itruediv__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        result = self.value / other[0]
        diff = result - self.value
        return self.__iadd__(Log(diff, other[1]))

    def init_metrics(self):
        self.logs.setdefault("_total", Stat())

    def reset(self):
        for key, val in self.logs.items():
            val.reset()
        self.value = 0