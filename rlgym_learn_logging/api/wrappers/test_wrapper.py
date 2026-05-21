"""Module for the test wrapper"""

import math
from typing import Generic, List, Dict, Any

from rlgym.api import AgentID, StateType

from ...logging_utils import nest_dict

from ..rewards import Logged, LoggedReward
from ..wrappers.wrapper import LoggedWrapper


class TestWrapper(LoggedWrapper[AgentID, StateType], Generic[AgentID, StateType]):
    """A wrapper to test if a reward is "well-formed" """

    def __init__(self, reward_fn: LoggedReward, error_if_none: bool = False):
        """A wrapper to test if a reward is "well-formed"

        :param reward_fn: The reward function to test
        :param error_if_none: Whether to throw an error
            if the value is None. Defaults to False.
        """
        super().__init__(reward_fn)
        self._error_if_none = error_if_none

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        rewards = super().get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )

        assert len(rewards) == len(agents), (
            "Amount of rewards must match the amount of agents"
        )
        for agent in agents:
            _nested_logs = nest_dict(rewards[agent].get_logs())

            _sum = sum(_nested_logs.values())
            _value = rewards[agent].get_value()
            assert _value is not None, (
                f"{self.__class__.__name__} expected a value but got None"
            )

            assert math.isclose(_sum, _value, rel_tol=1e-5), (
                f"The sum of all the logs doesn't match + "
                f"the total value: (Expected {_value}, got {_sum})"
            )

            if self._error_if_none:
                assert _value is not None, "Value is None when expected to be populated"

        return rewards
