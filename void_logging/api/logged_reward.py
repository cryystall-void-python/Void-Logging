import copy
from abc import ABC
from typing import Any, List, Dict

from .._internal.logged_reward_manager import LoggedRewardManager
from ..logging_utils import REWARDS_HEADER

from rlgym.api import AgentID, StateType
from rlgym.api.rlgym import RewardFunction


class LoggedReward(RewardFunction, ABC):
    def __init__(self, name: str = "Logged reward", weight = 1.0):
        self.name = name
        self.reward = LoggedRewardManager()
        self.weight = weight

    def _prepare_player_logging(self, agent_id: AgentID):
        self.reward.set_current_player(agent_id)
        self.reward.reset()

    def _compute_player_logging(self, agent_id: AgentID, shared_info: dict[str, Any]):
        self.reward.add_to_total(float(self.reward))

        shared_info[REWARDS_HEADER][agent_id].update(self.get_players_logs(agent_id))

    def get_players_logs(self, agent_id: AgentID) -> dict[str, Any]:
        log_values: dict[str, dict] = {}

        for metric in self.reward.get_all_metrics():
            display_name = "" if metric == "_total" else copy.copy(metric)

            if display_name == "__temp":
                continue

            log_values.setdefault(
                self.name + ("" if display_name.strip() == "" else "/" + display_name),
                self.reward.get_value_for_player(agent_id, metric) * self.weight
            )

        return log_values

    def reset(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        if not self.reward.is_ready:
            self.reward.init(initial_state)