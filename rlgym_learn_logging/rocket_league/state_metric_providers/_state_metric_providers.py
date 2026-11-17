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
        self._start_tick: int | None = None
        self._last_tick: int | None = None

    def init_metric_value(
        self, initial_state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        # On reset, report the length (in ticks) of the episode that just ended
        _ep_length = (
            None
            if self._start_tick is None or self._last_tick is None
            else self._last_tick - self._start_tick
        )
        self._start_tick = self._last_tick = initial_state.tick_count
        return _ep_length

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        self._last_tick = state.tick_count
        return None


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
