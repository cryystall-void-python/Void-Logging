from abc import ABC, abstractmethod
from typing import List, Dict, Any

from rlgym.api import SharedInfoProvider, AgentID, StateType


class MetricSharedInfoProvider(SharedInfoProvider, ABC):
    def __init__(self, metric_name: str):
        self._metric_name = metric_name

    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        shared_info[self._metric_name] = None
        return shared_info

class PlayerMetricSharedInfoProvider(MetricSharedInfoProvider, ABC):
    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        shared_info[self._metric_name] = None
        return shared_info

    @abstractmethod
    def init_metric_value_for(self, agent: AgentID, initial_state: StateType, shared_info: Dict[str, Any]) -> Any:
        """
        Called on the first step of the episode, gets the metric of a player, can be used to initialize stuff
        :param agent: Agent to get metric value from
        :param initial_state: The first state
        :param shared_info: Shared info
        :return: The metric of the player
        """
        pass

    @abstractmethod
    def get_metric_value_for(self, agent: AgentID, state: StateType, shared_info: Dict[str, Any]) -> Any:
        """
        Called on every other step of the episode, gets the metric of a player
        :param agent: Agent to get metric value from
        :param state: The first state
        :param shared_info: Shared info
        :return: The metric of the player
        """
        pass

    def set_state(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        del shared_info[self._metric_name]
        shared_info[self._metric_name] = {}

        for agent in agents:
            shared_info[self._metric_name][agent] = self.init_metric_value_for(agent, initial_state, shared_info)
        return shared_info

    def step(self, agents: List[AgentID], state: StateType, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        for agent in agents:
            shared_info[self._metric_name][agent] = self.get_metric_value_for(agent, state, shared_info)
        return shared_info

class MultiMetricSharedInfoProvider(SharedInfoProvider):
    def __init__(self, *metric_providers: MetricSharedInfoProvider):
        self._metric_providers = metric_providers

    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        for metric_provider in self._metric_providers:
            shared_info = metric_provider.create(shared_info=shared_info)
        return shared_info

    def set_state(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        for metric_provider in self._metric_providers:
            shared_info = metric_provider.set_state(agents, initial_state, shared_info)
        return shared_info

    def step(self, agents: List[AgentID], state: StateType, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        for metric_provider in self._metric_providers:
            shared_info = metric_provider.step(agents, state, shared_info)
        return shared_info

