"""Module for the default if none wrapper"""

from typing import Any, Dict, Generic, List

from rlgym.api import AgentID, StateType

from rlgym_learn_logging.api.rewards.logged_float import Logged

from ..rewards import LoggedReward
from ..wrappers.wrapper import LoggedWrapper


class DefaultIfNoneWrapper(
    LoggedWrapper[AgentID, StateType], Generic[AgentID, StateType]
):
    """A wrapper to replace a None value with a default value"""

    def __init__(self, reward_fn: LoggedReward, default_value: Any = 0):
        """A wrapper to replace a None value with a default value

        :param reward_fn: The reward function to correct
        :param default_value: The value to replace None with. Defaults to 0.
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
    ) -> Dict[AgentID, Logged]:
        _inner_rewards = super().get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )

        for agent in agents:
            if _inner_rewards[agent].get_value() is None:
                _inner_rewards[agent].value = self._default_value

        return _inner_rewards
