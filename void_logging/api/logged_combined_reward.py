from typing import List, Dict, Any, NamedTuple

from rlgym.api import AgentID, RewardFunction
from rlgym.rocket_league.api import GameState

from ..api.logged_reward import LoggedReward
from .._internal.logged_wrapper import LoggedWrapper

class LoggedCombinedRewardArg(NamedTuple):
    reward_fn: RewardFunction
    name: str = ""
    weight: float = 1.0

class LoggedCombinedReward(LoggedReward):
    def __init__(self, *rewards_and_weights: LoggedCombinedRewardArg, name: str = "Logged combined reward", weight: float = 1.0):
        """
        :param rewards_and_weights: A list of reward functions and their corresponding weights.
        """
        super().__init__(name, weight)
        reward_fns: List[LoggedReward] = []

        for value in rewards_and_weights:
            if not issubclass(type(value[0]), LoggedReward):
                r = LoggedWrapper(
                    value[0],
                    self.name +  "/" + type(value[0]).__name__ if value[1].strip() == "" else value[1],
                    self.weight * value[2]
                )
            else:
                r = value[0]
                r.weight *= self.weight * value[2]
                r.name = self.name + "/" + (value[1] if value[1].strip() != "" else r.name)

            reward_fns.append(r)

        self.reward_fns = tuple(reward_fns)

    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        super().reset(agents, initial_state, shared_info)
        for reward_fn in self.reward_fns:
            reward_fn.reset(agents, initial_state, shared_info)

    def get_rewards(self, agents: List[AgentID], state: GameState, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[str, Any]) -> Dict[AgentID, float]:
        # TODO optimize this double for loop with a numpy matrix?
        combined_rewards = {agent: 0. for agent in agents}
        for reward_fn in self.reward_fns:
            rewards = reward_fn.get_rewards(agents, state, is_terminated, is_truncated, shared_info)
            for agent, reward in rewards.items():
                combined_rewards[agent] += reward

        return combined_rewards