"""Module for the base providers for state and players"""

from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Any, Dict, List

from rlgym.rocket_league.api import GameState

from ..api.loggers.metric_provider import MetricSharedInfoProvider
from ..logging_utils import METRICS_HEADER, PLAYERS_METRICS_HEADER, STATE_METRICS_HEADER


class StateMetricSharedInfoProvider(MetricSharedInfoProvider[Hashable, GameState], ABC):
    """
    A shared info provider specially designed for state metrics (ball speed, scoreboard, etc...)
    """

    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        if METRICS_HEADER not in shared_info.keys():
            shared_info[METRICS_HEADER] = {}

        if STATE_METRICS_HEADER not in shared_info[METRICS_HEADER].keys():
            shared_info[METRICS_HEADER][STATE_METRICS_HEADER] = {}

        shared_info[METRICS_HEADER][STATE_METRICS_HEADER][self.metric_name] = None
        return shared_info

    def init_metric_value(
        self, initial_state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        """
        Called on the first step of the episode, gets the metric in the initial state,
        can be used to initialize stuff
        :param initial_state: The first state
        :param shared_info: Shared info
        :return: The metric of the state
        """
        return self.get_metric_value(initial_state, shared_info)

    @abstractmethod
    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        """
        Called on every other step of the episode, gets the metric of the state
        :param state: The first state
        :param shared_info: Shared info
        :return: The metric of the state
        """

    def set_state(
        self,
        agents: List[Hashable],
        initial_state: GameState,
        shared_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        shared_info[METRICS_HEADER][STATE_METRICS_HEADER][self.metric_name] = (
            self.init_metric_value(initial_state, shared_info)
        )
        return shared_info

    def step(
        self, agents: List[Hashable], state: GameState, shared_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        shared_info[METRICS_HEADER][STATE_METRICS_HEADER][self.metric_name] = (
            self.get_metric_value(state, shared_info)
        )
        return shared_info


class PlayerMetricSharedInfoProvider(
    MetricSharedInfoProvider[Hashable, GameState], ABC
):
    """A class to create a dict per agent within the METRICS_HEADER dict"""

    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        if METRICS_HEADER not in shared_info.keys():
            shared_info[METRICS_HEADER] = {}

        if PLAYERS_METRICS_HEADER not in shared_info[METRICS_HEADER].keys():
            shared_info[METRICS_HEADER][PLAYERS_METRICS_HEADER] = {}

        shared_info[METRICS_HEADER][PLAYERS_METRICS_HEADER][self.metric_name] = {}

        return shared_info

    def init_metric_value_for(
        self, agent: Hashable, initial_state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        """
        Called on the first step of the episode,
        gets the metric of a player, can be used to initialize stuff
        :param agent: Agent to get metric value from
        :param initial_state: The first state
        :param shared_info: Shared info
        :return: The metric of the player
        """
        return self.get_metric_value_for(agent, initial_state, shared_info)

    @abstractmethod
    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        """
        Called on every other step of the episode, gets the metric of a player
        :param agent: Agent to get metric value from
        :param state: The first state
        :param shared_info: Shared info
        :return: The metric of the player
        """

    def set_state(
        self,
        agents: List[Hashable],
        initial_state: GameState,
        shared_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        for agent in agents:
            shared_info[METRICS_HEADER][PLAYERS_METRICS_HEADER][self.metric_name][
                agent
            ] = self.init_metric_value_for(agent, initial_state, shared_info)
        return shared_info

    def step(
        self, agents: List[Hashable], state: GameState, shared_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        for agent in agents:
            shared_info[METRICS_HEADER][PLAYERS_METRICS_HEADER][self.metric_name][
                agent
            ] = self.get_metric_value_for(agent, state, shared_info)
        return shared_info
