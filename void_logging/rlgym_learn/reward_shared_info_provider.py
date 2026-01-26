"""Module for the reward shared info provider"""

from typing import Generic, List, Dict, Any

from rlgym.api import SharedInfoProvider, AgentID, StateType

from ..logging_utils import REWARDS_HEADER


class RewardSharedInfoProvider(
    SharedInfoProvider[AgentID, StateType], Generic[AgentID, StateType]
):
    """This class is used to create a dictionary
    within shared_info[REWARDS_HEADER] with each agent within"""

    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        if REWARDS_HEADER not in shared_info:
            shared_info[REWARDS_HEADER] = {}
        return shared_info

    def set_state(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        for agent in agents:
            shared_info[REWARDS_HEADER][agent] = {}
        return shared_info

    def step(
        self, agents: List[AgentID], state: StateType, shared_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        return shared_info
