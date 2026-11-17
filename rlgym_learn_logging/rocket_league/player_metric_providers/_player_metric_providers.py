"""Module for all the player metric providers"""

from collections.abc import Hashable
from typing import Dict, Any
import numpy as np

from rlgym.rocket_league.api import GameState

from ...rocket_league.metric_providers import PlayerMetricSharedInfoProvider


class PlayerVelocityMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's velocity inside the shared info
    """

    @property
    def metric_name(self) -> str:
        return "Player/Velocity"

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        return float(np.linalg.norm(state.cars[agent].physics.linear_velocity))


class PlayerHeightMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's height inside the shared info
    """

    @property
    def metric_name(self) -> str:
        return "Player/Height"

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        return float(state.cars[agent].physics.position[2])


class PlayerTouchMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's amount of touches inside the shared info
    """

    def __init__(self, use_ratio: bool = True):
        """
        Sets the player's amount of touches inside the shared info
        :param use_ratio: Whether you want touch ratio or amount of touches
        """
        self._use_ratio = use_ratio

    @property
    def metric_name(self) -> str:
        return "Player/Touch"

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        n_touches = state.cars[agent].ball_touches

        # If you want touch ratio (Tendency of bot to touch the ball)
        if self._use_ratio:
            return float(n_touches)

        # If you want the amount of touches
        if n_touches > 0:
            return float(n_touches)
        return None


class PlayerBoostAmountMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's boost amount inside the shared info
    """

    @property
    def metric_name(self) -> str:
        return "Player/Boost amount"

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        return state.cars[agent].boost_amount


class PlayerBallHitForceMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Whenever a player hits the ball, it puts the hit force info inside the shared info

    Hit force is considered as the ball acceleration on ball's touch: the change
    of ball velocity over the step of the touch, per tick (uu/s per tick)
    """

    @property
    def metric_name(self) -> str:
        return "Player/Hit force"

    def __init__(self):
        # Ball velocity and tick of the previous step, per agent (this provider
        # is called once per agent per step)
        self._last: Dict[Hashable, tuple[np.ndarray, int]] = {}

    def init_metric_value_for(
        self, agent: Hashable, initial_state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        self._last[agent] = (
            initial_state.ball.linear_velocity.copy(),
            initial_state.tick_count,
        )
        return None

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        _last_ball_vel, _last_tick_count = self._last[agent]
        # Updated every step, so a touch is compared with the step just before it
        self._last[agent] = (state.ball.linear_velocity.copy(), state.tick_count)
        if state.cars[agent].ball_touches == 0:
            return None
        _tick_count = max(1, state.tick_count - _last_tick_count)
        _ball_accel = (state.ball.linear_velocity - _last_ball_vel) / _tick_count
        return float(np.linalg.norm(_ball_accel))


class PlayerOnGroundRatioMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """A provider that gives the player on ground ratio"""

    @property
    def metric_name(self) -> str:
        return "Player/On ground"

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        return state.cars[agent].on_ground


class PlayerBallHitHeightMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """A provider that gives the player's hit height"""

    @property
    def metric_name(self) -> str:
        return "Player/Hit height"

    def get_metric_value_for(
        self, agent: Hashable, state: GameState, shared_info: Dict[str, Any]
    ) -> float | None:
        if state.cars[agent].ball_touches > 0:
            return float(state.ball.position[2])
        return None
