"""Module for the apply operation wrapper"""

from typing import Any, Callable, Dict, Generic, List

from rlgym.api import AgentID, StateType

from rlgym_learn_logging.api.rewards import Log, Logged, LoggedReward
from rlgym_learn_logging.api.wrappers.wrapper import LoggedWrapper


class ApplyOperationWrapper(
    LoggedWrapper[AgentID, StateType], Generic[AgentID, StateType]
):
    """A wrapper that applies an operation to the inner reward"""

    USER_OPERATION_METRIC: str = "User operation"

    def __init__(
        self, reward_fn: LoggedReward, operation: Callable[[Any], Any] = lambda x: x
    ):
        super().__init__(reward_fn)
        self._operation = operation

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
            reward_value = rewards[agent].get_value()
            assert reward_value is not None, (
                f"{self.__class__.__name__} expects a value to apply "
                + "the operation, but got None"
            )
            _transformed_value = self._operation(reward_value)
            _difference = _transformed_value - reward_value

            rewards[agent] += Log(value=_difference, metric=self.USER_OPERATION_METRIC)

        return rewards

    @property
    def metrics(self) -> list[str]:
        return super().metrics + [self.USER_OPERATION_METRIC]
