from typing import Callable, List, Dict, Any

from rlgym.api import AgentID, StateType

from void_logging.api.rewards import LoggedReward, Logged, Log
from void_logging.api.wrappers import LoggedWrapper


class ApplyOperationWrapper(LoggedWrapper):
    USER_OPERATION_METRIC: str = "User operation"

    def __init__(self, reward_fn: LoggedReward, operation: Callable[[float], float] = lambda x: x):
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
        rewards = super().get_rewards(agents, state, is_terminated, is_truncated, shared_info)

        for agent in agents:
            _transformed_value = self._operation(rewards[agent].get_value())
            _difference = _transformed_value - rewards[agent].get_value()

            rewards[agent] += Log(value=_difference, metric=self.USER_OPERATION_METRIC)

        return rewards

    @property
    def metrics(self) -> list[str]:
        return super().metrics + [self.USER_OPERATION_METRIC]