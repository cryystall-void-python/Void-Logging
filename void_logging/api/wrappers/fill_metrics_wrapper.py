"""Module for the fill metrics wrapper"""

from typing import Generic, List, Dict, Any

from rlgym.api import AgentID, StateType

from void_logging.api.rewards import Logged, Log
from void_logging.api.wrappers.wrapper import LoggedWrapper


class FillMetricsWrapper(
    LoggedWrapper[AgentID, StateType], Generic[AgentID, StateType]
):
    """
    A wrapper to trigger the metrics even though they were not triggered
    """

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

        for agent in agents:
            for metric in self.metrics:
                # Populate with empty log
                rewards[agent] += Log(value=0, metric=metric)

        return rewards
