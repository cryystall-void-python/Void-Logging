"""Module for the base logged wrapper class"""

import re
from typing import Generic, List, Dict, Any

from rlgym.api import AgentID, StateType, RewardFunction

from ..rewards import Logged, LoggedReward


class LoggedWrapper(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    """A wrapper to act on an inner reward"""
    @property
    def name(self) -> str:
        """
        The name that will appear (unless overridden) in the final logging
        :return: The final name
        """
        try:
            return self._reward_fn.name  # pyright: ignore[reportAttributeAccessIssue] # noqa Will get caught inside the error if it doesn't exists
        except AttributeError:
            _separated = re.findall("[A-Z][^A-Z]*", type(self._reward_fn).__name__)
            return (
                " ".join(_separated[:-1])
                if _separated[-1] == "Reward"
                else " ".join(_separated)
            )

    def __init__(self, reward_fn: RewardFunction):
        """
        A wrapper to apply an operation on a reward function

        Args:
            reward_fn (RewardFunction): The reward function to work with
        """
        self._reward_fn = reward_fn
        self._is_reward_fn_logged = isinstance(reward_fn, LoggedReward) or issubclass(
            type(reward_fn), LoggedReward
        )

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        return self._reward_fn.get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        self._reward_fn.reset(agents, initial_state, shared_info)

    @property
    def metrics(self) -> list[str]:
        try:
            return self._reward_fn.metrics  # pyright: ignore[reportAttributeAccessIssue] # noqa If metrics not in the attributes list, return nothing
        except AttributeError:
            return []
