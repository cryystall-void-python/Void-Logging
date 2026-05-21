"""Module for all the state providers"""

from typing import Dict, Any

import numpy as np
from rlgym.rocket_league.api import GameState
from rlgym.rocket_league.common_values import UNREAL_UNITS_PER_METER

from ..metric_providers import StateMetricSharedInfoProvider


class GoalMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    """
    Set the goal ratio/amount of goals in the shared info
    """

    def __init__(self, use_ratio: bool = True):
        """
        Set the goal ratio/amount of goals in the shared info
        :param use_ratio: Whether you want goal ratio or amount of goals
        """
        self._use_ratio = use_ratio

    @property
    def metric_name(self) -> str:
        return "Misc/Goals"

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        # If you want goal ratio (Tendency of bot to score)
        if self._use_ratio:
            return float(state.goal_scored)

        # If you want the amount of goals
        if state.goal_scored:
            return 1
        return None


class EpisodeLengthSharedInfoProvider(StateMetricSharedInfoProvider):
    """
    Sets the episode length inside the shared info if episode is finished
    """

    @property
    def metric_name(self) -> str:
        return "Misc/Episode Length"

    def __init__(self):
        self._episode_length = 0

    def init_metric_value(
        self, initial_state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        if self._episode_length != 0:  # Reset called after an episode
            _ep_length = self._episode_length
            self._episode_length = 0
            return _ep_length
        return None

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        self._episode_length = state.tick_count - self._episode_length


class GoalScoreSpeedSharedInfoProvider(StateMetricSharedInfoProvider):
    """A provider that gives the goal score speed"""

    @property
    def metric_name(self) -> str:
        return "Misc/Goal speed (kph)"

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        if state.goal_scored:
            _mps_speed = (
                np.linalg.norm(state.ball.linear_velocity) / UNREAL_UNITS_PER_METER
            )  # uu/s to m/s
            _kph_speed = _mps_speed * 3.6  # m/s to km/h
            return float(_kph_speed)
        return None
