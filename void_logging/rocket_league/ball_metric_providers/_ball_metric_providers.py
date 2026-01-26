"""Module for all the ball metrics providers"""

from typing import Dict, Any

import numpy as np
from rlgym.rocket_league.api import GameState

from ...rocket_league.metric_providers import StateMetricSharedInfoProvider


class BallVelocityMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    """A provider that gives the ball velocity"""

    @property
    def metric_name(self) -> str:
        return "Ball/Velocity"

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        return float(np.linalg.norm(state.ball.linear_velocity))


class BallHeightMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    """A provider that gives the ball height"""

    @property
    def metric_name(self) -> str:
        return "Ball/Height"

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        return float(state.ball.position[2])


class BallAccelerationMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    """A provider that gives the ball acceleration"""

    @property
    def metric_name(self) -> str:
        return "Ball/Acceleration"

    def __init__(self, count_deceleration: bool = False):
        self._count_deceleration = count_deceleration

        self._last_velocity = 0
        self._last_tick_count = 0

    def init_metric_value(
        self, initial_state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        # This is first tick, so no division, just return 0 and set things up

        self._last_velocity = np.linalg.norm(initial_state.ball.linear_velocity)
        self._last_tick_count = initial_state.tick_count

        return 0

    def get_metric_value(
        self, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        _current_vel = np.linalg.norm(state.ball.linear_velocity)
        _current_tick_count = state.tick_count

        _accel_raw = _current_vel - self._last_velocity

        if not self._count_deceleration:
            _accel_raw = max(0, _accel_raw)

        _accel = _accel_raw / (_current_tick_count - self._last_tick_count)

        self._last_velocity = _current_vel
        self._last_tick_count = _current_tick_count

        return float(_accel)
