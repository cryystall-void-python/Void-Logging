"""Module for the condition wrapper"""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Dict

from rlgym.api import AgentID, StateType

from ..rewards import Logged
from ..wrappers.wrapper import LoggedWrapper


class ConditionWrapper(
    LoggedWrapper[AgentID, StateType], ABC, Generic[AgentID, StateType]
):
    """A wrapper to only call get_rewards if a condition is respected"""

    @abstractmethod
    def condition(
        self, agents: list[AgentID], state: StateType, shared_info: dict[str, Any]
    ) -> dict[AgentID, bool]:
        """The condition to trigger the reward

        :param agents: All the agents to test
        :param state: The state to test them on
        :param shared_info: The environment's shared info

        :return: agent_cond (dict[AgentID, bool]): A dict giving the info of whether an agent
                will trigger the reward / triggered the condition
        """

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        _agents_conditions = self.condition(agents, state, shared_info)
        _trigger_condition_agents = [
            agent for agent in agents if _agents_conditions[agent]
        ]

        _inner_rewards = super().get_rewards(
            _trigger_condition_agents, state, is_terminated, is_truncated, shared_info
        )

        for agent in agents:
            # If the agent doesn't satisfy the condition
            if not _agents_conditions[agent]:
                _inner_rewards[agent] = Logged()

        return _inner_rewards
