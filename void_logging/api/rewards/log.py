"""Module for the Log class"""

from typing import Any

from pydantic import BaseModel

SEPARATOR = "/"


class Log(BaseModel, extra="forbid"):
    """A class to store a value and a metric"""

    value: Any
    metric: str

    def __mul__(self, other: Any):
        _new_log = self.model_copy()
        _new_log.value *= other
        return _new_log

    def __imul__(self, other: Any):
        self.value *= other
        return self
