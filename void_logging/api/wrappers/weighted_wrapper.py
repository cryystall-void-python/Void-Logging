from typing import List, Dict, Any

from rlgym.api import AgentID, StateType, RewardType

from ..rewards import Log, LoggedReward
from ..wrappers import LoggedWrapper


class WeightedWrapper(LoggedWrapper):
    def __init__(
        self,
        reward_fn: LoggedReward,
        weight: float = 1.0,
        propagate_to_logs: bool = True,
    ):
        """
        A class to weight a reward
        :param reward_fn: The reward function to weight
        :param weight: The weight you need to apply
        :param propagate_to_logs: Whether you want to see the weighted metrics or another field called "Weight" that shows the impact of the weight on the final value
        """
        super().__init__(reward_fn)
        self._weight = weight
        self._propagate_to_logs = propagate_to_logs

    @property
    def weight(self):
        return self._weight

    @property
    def is_weight_propagated_to_logs(self):
        return self._propagate_to_logs

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
            assert _inner_rewards[agent].get_value() is not None, (
                f"{self.name} ({self.__class__.__name__}) expects a value but got None"
            )

            if self.is_weight_propagated_to_logs:
                _inner_rewards[agent].apply_operation_to_logs(
                    lambda val: val * self.weight
                )
                _inner_rewards[agent].value *= self.weight
            else:
                _inner_rewards[agent] *= Log(value=self.weight, metric="Weight")

        return _inner_rewards

    @property
    def metrics(self) -> list[str]:
        if self._propagate_to_logs:
            return super().metrics
        return super().metrics + ["Weight"]
