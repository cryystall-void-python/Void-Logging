from typing import Dict, Any

from rlgym.api import StateType
from rlgym.rocket_league.api import GameState

from void_logging.api.loggers.metric_provider import StateMetricSharedInfoProvider
import numpy as np


class BallVelocityMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Ball/Velocity"):
        super().__init__(metric_name)

    def get_metric_value(self, state: GameState, shared_info: Dict[str, Any]):
        return np.linalg.norm(state.ball.linear_velocity)

class BallHeightMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Ball/Height"):
        super().__init__(metric_name)

    def get_metric_value(self, state: GameState, shared_info: Dict[str, Any]):
        return state.ball.position[2]

class BallAccelerationMetricSharedInfoProvider(StateMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Ball/Acceleration", count_deceleration: bool = False):
        super().__init__(metric_name)

        self._count_deceleration = count_deceleration

        self._last_velocity = 0
        self._last_tick_count = 0

    def init_metric_value(self, initial_state: GameState, shared_info: Dict[str, Any]):
        # This is first tick, so no division, just return 0 and set things up

        self._last_velocity = np.linalg.norm(initial_state.ball.linear_velocity)
        self._last_tick_count = initial_state.tick_count

        return 0

    def get_metric_value(self, state: GameState, shared_info: Dict[str, Any]):
        _current_vel = np.linalg.norm(state.ball.linear_velocity)
        _current_tick_count = state.tick_count

        _accel_raw = _current_vel - self._last_velocity

        if self._count_deceleration:
            _accel_raw = max(0, _accel_raw)

        _accel = _accel_raw / (_current_tick_count - self._last_tick_count)

        self._last_velocity = _current_vel
        self._last_tick_count = _current_tick_count

        return _accel