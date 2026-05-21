"""Module for the base metric provider"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic

from rlgym.api import AgentID, SharedInfoProvider, StateType

from rlgym_learn_logging.logging_utils import METRICS_HEADER


class MetricSharedInfoProvider(
    Generic[AgentID, StateType], SharedInfoProvider[AgentID, StateType], ABC
):
    """
    A shared info provider adding stuff in the metrics shared info
    """

    @property
    @abstractmethod
    def metric_name(self) -> str:
        """Returns the name that will be used to fill the shared info with"""

    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        if METRICS_HEADER not in shared_info.keys():
            shared_info[METRICS_HEADER] = {}

        shared_info[METRICS_HEADER][self.metric_name] = None
        return shared_info
