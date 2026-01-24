"""Module for the Logged class"""

from collections.abc import Callable
from typing import Generic

from pydantic import BaseModel
from typing_extensions import TypeVar

from .log import Log, SEPARATOR

LoggedKlassType = TypeVar("LoggedKlassType", default=float)


class Logged(BaseModel, Generic[LoggedKlassType]):
    """A class used to track the evolution of a value by using the Log class"""
    logs: dict[str, LoggedKlassType] = {}
    value: LoggedKlassType | None = None

    def __del__(self):
        self.logs.clear()

    def sanitize(self):
        """Cleans the logs if the value is empty"""
        for _key in self.logs.copy():
            if self.logs[_key] is None:
                self.logs.pop(_key)

    def get_value(self) -> LoggedKlassType | None:
        """Gets the value currently being stored

        Returns:
            value (LoggedKlassType | None): The current value
        """
        return self.value

    def get_log_value(self, log_name: str) -> LoggedKlassType | None:
        """Gets the value of a log

        Args:
            log_name (str): The log you need to get the value of

        Returns:
            log_value (LoggedKlassType | None): The value of the log
        """
        return self.logs.get(log_name)

    def __iadd__(self, other):
        log = Log.model_validate(other)

        # If the value is a Logged, merge the logs and regroup them under the metric name
        # So, if given the "test" metric, you'll have
        # test/metric1
        # test/metric2
        # Etc...
        if isinstance(log.value, Logged) or issubclass(type(log.value), type(Logged)):
            for _metric in log.value.get_logs().keys():
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
            for _metric in log.value.get_logs().keys():
                _modified_metric = (
                    log.metric + (SEPARATOR + _metric)
                    if len(_metric.strip()) != 0
                    else ""
                )

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

    def apply_operation_to_logs(self, fn: Callable[[LoggedKlassType], LoggedKlassType]):
        """Apply an operation to a log

        Args:
            fn (Callable[[LoggedKlassType], LoggedKlassType]): The operation to apply
        """
        self.logs = {k: fn(v) for k, v in self.logs.items()}

    def get_logs(self) -> dict[str, LoggedKlassType]:
        """Gets all the logs

        Returns:
            logs (dict[str, LoggedKlassType]): All the logs
        """
        return self.logs
