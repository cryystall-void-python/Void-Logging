from typing import List, Dict, Any

from rlgym.api import AgentID, StateType, RewardType, RewardFunction

from .._internal.logged_float import Log
from ..api.logged_reward import LoggedReward


class LoggedWrapper(LoggedReward):
    def __init__(self, reward_fn: RewardFunction, name: str, weight: float = 1.0):
        super().__init__(name, weight)
        self.reward_fn = reward_fn

    def get_rewards(self, agents: List[AgentID], state: StateType, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[str, Any]) -> Dict[AgentID, RewardType]:
        rewards = self.reward_fn.get_rewards(agents, state, is_terminated, is_truncated, shared_info)

        for agent in agents:
            self._prepare_player_logging(agent)

            self.reward += Log(rewards[agent], "__temp")

            self._compute_player_logging(agent, shared_info)

        return rewards

    def reset(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        super().reset(agents, initial_state, shared_info)
        self.reward_fn.reset(agents, initial_state, shared_info)