"""Module for the weighted wrapper"""

from typing import Generic, List, Dict, Any

from rlgym.api import AgentID, StateType

from ..rewards import Log, LoggedReward, Logged
from ..wrappers.wrapper import LoggedWrapper


class WeightedWrapper(LoggedWrapper[AgentID, StateType], Generic[AgentID, StateType]):
    """A class to weight a reward"""

    def __init__(
        self,
        reward_fn: LoggedReward,
        weight: float = 1.0,
        propagate_to_logs: bool = True,
    ):
        """
        A class to weight a reward

        Args:
            reward_fn (LoggedReward): The reward function to weight
            weight (float, optional): The weight you need to apply. Defaults to 1.0.
            propagate_to_logs (bool, optional): Whether you want to see the
                weighted metrics or another field called "Weight" that shows the
                impact of the weight on the final value. Defaults to True.
        """
        super().__init__(reward_fn)
        self.weight = weight
        self.propagate_to_logs = propagate_to_logs

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
            assert _inner_rewards[agent].get_value() is not None, (
                f"{self.name} ({self.__class__.__name__}) expects a value but got None"
            )

            if self.propagate_to_logs:
                _inner_rewards[agent].apply_operation_to_logs(
                    lambda val: val * self.weight
                )
                _inner_rewards[
                    agent
                ].value *= self.weight  # TODO: Make a set_value method
            else:
                _inner_rewards[agent] *= Log(value=self.weight, metric="Weight")

        return _inner_rewards

    @property
    def metrics(self) -> list[str]:
        if self.propagate_to_logs:
            return super().metrics
        return super().metrics + ["Weight"]
