from typing import Dict, Any

from rlgym.api import AgentID
from rlgym.rocket_league.api import GameState

from void_logging.api.loggers import PlayerMetricSharedInfoProvider
import numpy as np

class PlayerVelocityMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Player/Velocity"):
        super().__init__(metric_name)

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> Any:
        return np.linalg.norm(state.cars[agent].physics.linear_velocity)

class PlayerHeightMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Player/Height"):
        super().__init__(metric_name)

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> Any:
        return state.cars[agent].physics.position[2]

class PlayerTouchMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Player/Touch"):
        super().__init__(metric_name)

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> Any:
        return state.cars[agent].ball_touches

class PlayerBoostAmountMetricSharedInfoProvider(PlayerMetricSharedInfoProvider):
    def __init__(self, metric_name: str = "Player/Boost"):
        super().__init__(metric_name)

    def get_metric_value_for(self, agent: AgentID, state: GameState, shared_info: Dict[str, Any]) -> Any:
        return state.cars[agent].boost_amount