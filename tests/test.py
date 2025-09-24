from typing import List, Dict, Any

from rlgym.api import StateType, AgentID, RewardType

from void_logging import LoggedReward, Log

class DummyReward(LoggedReward):

    def __init__(self, name: str = "Dummy reward", weight: float = 1.0):
        super().__init__(name, weight)

    def get_rewards(self, agents: List[AgentID], state: StateType, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[str, Any]) -> Dict[AgentID, RewardType]:
        rewards = {agent: 0.0 for agent in agents}

        for agent in agents:
            self._prepare_player_logging(agent)

            self.reward += Log(8.0, "Test addition")
            self.reward -= Log(4.0, "Test subtraction")
            self.reward *= Log(3.0, "Test multiplication")
            self.reward /= Log(2.0, "Test division")

            self._compute_player_logging(agent, shared_info)
            rewards[agent] = float(self.reward)

        return rewards