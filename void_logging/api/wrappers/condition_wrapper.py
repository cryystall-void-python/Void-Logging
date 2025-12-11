from abc import ABC, abstractmethod
from typing import Any, List, Dict

from rlgym.api import AgentID, StateType

from ..rewards import Logged
from ..wrappers import LoggedWrapper


class ConditionWrapper(LoggedWrapper, ABC):
    @abstractmethod
    def condition(
        self, agents: list[AgentID], state: StateType, shared_info: dict[str, Any]
    ) -> dict[AgentID, bool]:
        pass

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
