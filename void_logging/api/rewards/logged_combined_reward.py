from typing import List, Dict, Any

from rlgym.api import AgentID, StateType, RewardType
from void_logging.api.rewards.log import SEPARATOR

from .log import Log
from .logged_float import Logged
from .logged_reward import LoggedReward


class LoggedCombinedReward(LoggedReward):
    @property
    def name(self) -> str:
        return "Logged combined reward"

    def __init__(self, *rewards_and_weights: LoggedReward):
        """
        :param rewards_and_weights: A list of reward functions and their corresponding weights.
        """
        self._reward_fns: List[LoggedReward] = list(rewards_and_weights)

    @property
    def reward_functions(self) -> List[LoggedReward]:
        """
        All the reward functions of the combined reward
        :return: All the reward functions of the combined reward
        """
        return self._reward_fns

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, RewardType]:
        rewards = {agent: Logged() for agent in agents}

        for reward_fn in self.reward_functions:
            _inner_rewards = reward_fn.get_rewards(
                agents, state, is_terminated, is_truncated, shared_info
            )
            for agent, reward in _inner_rewards.items():
                rewards[agent] += Log(metric=reward_fn.name, value=reward)

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        for reward_fn in self.reward_functions:
            reward_fn.reset(agents, initial_state, shared_info)

    @property
    def metrics(self) -> list[str]:
        _metrics = []
        for reward_fn in self.reward_functions:
            _metrics += [
                reward_fn.name + SEPARATOR + metric for metric in reward_fn.metrics
            ]
            _metrics.append(reward_fn.name)

        return _metrics
