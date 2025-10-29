from typing import Dict, Any

from rlgym.api import AgentID
from rlgym.rocket_league.api import GameState

from ...rocket_league.metric_providers import PlayerMetricSharedInfoProvider
import numpy as np


class PlayerVelocityMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's velocity inside the shared info
    """

    @property
    def metric_name(self) -> str:
        return "Player/Velocity"

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
        return float(np.linalg.norm(state.cars[agent].physics.linear_velocity))


class PlayerHeightMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's height inside the shared info
    """

    @property
    def metric_name(self) -> str:
        return "Player/Height"

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
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

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
        n_touches = state.cars[agent].ball_touches

        # If you want touch ratio (Tendency of bot to touch the ball)
        if self._use_ratio:
            return float(n_touches)

        # If you want the amount of touches
        if n_touches > 0:
            return float(n_touches)


class PlayerBoostAmountMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Sets the player's boost amount inside the shared info
    """

    @property
    def metric_name(self) -> str:
        return "Player/Boost amount"

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
        return state.cars[agent].boost_amount


class PlayerBallHitForceMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    """
    Whenever a player hits the ball, it puts the hit force info inside the shared info

    Hit force is considered as the ball acceleration on ball's touch
    """

    @property
    def metric_name(self) -> str:
        return "Player/Hit force"

    def __init__(self):
        self._last_ball_vel = None
        self._last_tick_count = 0

    def init_metric_value_for(self, agent: AgentID, initial_state: GameState,
                              shared_info: Dict[str, Any]) -> float | None:
        self._last_ball_vel = initial_state.ball.linear_velocity
        self._last_tick_count = initial_state.tick_count

        return None

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
        if state.cars[agent].ball_touches > 0:
            _ball_accel = state.ball.linear_velocity - self._last_ball_vel
            _tick_count = state.tick_count - self._last_tick_count

            _ball_accel /= _tick_count

            self._last_ball_vel = state.ball.linear_velocity
            self._last_tick_count = state.tick_count

            return float(np.linalg.norm(_ball_accel))

class PlayerOnGroundRatioMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    @property
    def metric_name(self) -> str:
        return "Player/On ground"

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
        return state.cars[agent].on_ground

class PlayerBallHitHeightMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    @property
    def metric_name(self) -> str:
        return "Player/Hit height"

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> float | None:
        if state.cars[agent].ball_touches > 0:
            return float(state.ball.position[2])
        return None