from typing import Any

from pydantic import BaseModel

SEPARATOR = "/"


class Log(BaseModel, extra="forbid"):
    value: Any
    metric: str

    def __mul__(self, other):
        _new_log = self.model_copy()
        _new_log.value *= other
        return _new_log

    def __imul__(self, other):
        self.value *= other
        return self
