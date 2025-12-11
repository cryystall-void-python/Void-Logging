from typing import List, Dict, Any

from rlgym.api import AgentID, StateType, RewardType

from ..rewards import LoggedReward
from ..wrappers import LoggedWrapper


class DefaultIfNoneWrapper(LoggedWrapper):
    def __init__(self, reward_fn: LoggedReward, default_value: float = 0):
        """
        A wrapper to replace a None value with a default value
        :param reward_fn: The reward function to correct
        :param default_value: The value to replace None with
        """
        super().__init__(reward_fn)
        self._default_value = default_value

    @property
    def default_value(self):
        """
        The default value replacing None values
        :return: The default value
        """
        return self._default_value

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, RewardType]:
        _inner_rewards = super().get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )

        for agent in agents:
            if _inner_rewards[agent].get_value() is None:
                _inner_rewards[agent].value = self._default_value

        return _inner_rewards
