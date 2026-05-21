"""Module for the reward function wrapper"""

from typing import Generic, List, Dict, Any

from rlgym.api import AgentID, StateType, RewardFunction

from ..rewards import LoggedReward, Log, Logged
from ..wrappers.wrapper import LoggedWrapper


class RewardFnWrapper(LoggedWrapper[AgentID, StateType], Generic[AgentID, StateType]):
    """A wrapper that transform a non logged reward to a logged reward"""

    REWARD_VALUE_METRIC: str = "Reward value"

    def __init__(self, reward_fn: RewardFunction):
        super().__init__(reward_fn)

        if issubclass(type(reward_fn), LoggedReward):
            raise ValueError(
                f"The wrapper {self.__class__.__name__} is meant to be used with "
                + f"the type {RewardFunction.__name__}, you used it with "
                + f"the type {type(reward_fn).__name__}"
            )
        self._is_reward_fn_logged = True

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        _inner_rewards = self._reward_fn.get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )
        rewards = {agent: Logged() for agent in agents}

        for agent in agents:
            rewards[agent] += Log(
                value=_inner_rewards[agent], metric=self.REWARD_VALUE_METRIC
            )

        return rewards

    @property
    def metrics(self) -> list[str]:
        return super().metrics + []
