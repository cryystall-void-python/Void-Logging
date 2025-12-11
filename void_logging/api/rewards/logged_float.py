from collections.abc import Callable
from typing import Generic

from pydantic import BaseModel
from typing_extensions import TypeVar

from .log import Log, SEPARATOR

LoggedKlassType = TypeVar("LoggedKlassType", default=float)


class Logged(BaseModel, Generic[LoggedKlassType]):
    logs: dict[str, LoggedKlassType] = {}
    value: LoggedKlassType | None = None

    def __del__(self):
        self.logs.clear()

    def sanitize(self):
        for _key in self.logs.copy():
            if self.logs[_key] is None:
                self.logs.pop(_key)

    def get_value(self):
        return self.value

    def get_log_value(self, log_name: str):
        return self.logs.get(log_name)

    def __iadd__(self, other):
        log = Log.model_validate(other)

        # If the value is a Logged, merge the logs and regroup them under the metric name
        # So, if given the "test" metric, you'll have
        # test/metric1
        # test/metric2
        # Etc...
        if isinstance(log.value, Logged) or issubclass(type(log.value), type(Logged)):
            for _metric, _value in log.value.get_logs().items():
                _modified_metric = (
                    log.metric + (SEPARATOR + _metric)
                    if len(_metric.strip()) != 0
                    else ""
                )

                if _modified_metric not in self.logs.keys():
                    self.logs[_modified_metric] = log.value.get_log_value(_metric)
                else:
                    self.logs[_modified_metric] = self.logs.get(
                        _modified_metric
                    ) + log.value.get_log_value(_metric)

            if log.metric not in self.logs.keys():
                self.logs[log.metric] = log.value.get_value()
            else:
                self.logs[log.metric] = (
                    self.logs.get(log.metric) + log.value.get_value()
                )

            if not self.value:
                self.value = log.value.get_value()
            else:
                self.value += log.value.get_value()
        else:
            if log.metric not in self.logs.keys():
                self.logs[log.metric] = log.value
            else:
                self.logs[log.metric] = self.logs.get(log.metric) + log.value

            if not self.value:
                self.value = log.value
            else:
                self.value += log.value

        return self

    def __isub__(self, other):
        log = Log.model_validate(other)

        # If the value is a Logged, merge the logs
        if isinstance(log.value, Logged) or issubclass(type(log.value), type(Logged)):
            for _metric, _value in log.value.get_logs().items():
                _modified_metric = ""
                if len(log.metric.strip()) != 0:
                    _modified_metric = log.metric

                if len(_metric.strip()) != 0:
                    _modified_metric += SEPARATOR - _metric

                if _modified_metric not in self.logs.keys():
                    self.logs[_modified_metric] = -log.value.get_log_value(_metric)
                else:
                    self.logs[_modified_metric] = self.logs.get(
                        _modified_metric
                    ) - log.value.get_log_value(_metric)

            if log.metric not in self.logs.keys():
                self.logs[log.metric] = log.value.get_value()
            else:
                self.logs[log.metric] = (
                    self.logs.get(log.metric) + log.value.get_value()
                )

            if not self.value:
                self.value = -log.value.get_value()
            else:
                self.value -= log.value.get_value()
        else:
            if log.metric not in self.logs.keys():
                self.logs[log.metric] = -log.value
            else:
                self.logs[log.metric] = self.logs.get(log.metric) - log.value

            if not self.value:
                self.value = -log.value
            else:
                self.value -= log.value
        return self

    def __imul__(self, other):
        log = Log.model_validate(other)

        diff = (log.value - 1) * self.get_value()
        return self.__iadd__(Log(value=diff, metric=log.metric))

    def __itruediv__(self, other):
        log = Log.model_validate(other)

        result = self.get_value() / log.value
        diff = result - self.get_value()
        return self.__isub__(Log(value=diff, metric=log.metric))

    def _apply_weight(self, weight: float | int):
        for _metric in self.logs.keys():
            self.logs[_metric] *= weight

        if self.value:
            self.value *= weight

    def apply_operation_to_logs(self, fn: Callable[[LoggedKlassType], LoggedKlassType]):
        self.logs = {k: fn(v) for k, v in self.logs.items()}

    def get_logs(self):
        return self.logs
