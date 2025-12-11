from typing import Self, Callable

from void_logging.api.wrappers import (
    LoggedWrapper,
    ZeroSumWrapper,
    WeightedWrapper,
    CustomNameWrapper,
    DefaultIfNoneWrapper,
    RewardFnWrapper,
)
from void_logging.api.wrappers.apply_operation_wrapper import ApplyOperationWrapper
from void_logging.api.wrappers.debug_wrapper import DebugWrapper
from void_logging.api.wrappers.fill_metrics_wrapper import FillMetricsWrapper


class ChainWrapper(LoggedWrapper):
    """
    A wrapper to allow the use of chain functions
    """
    def zero_sum(self, team_spirit: float = 0.0, opp_scaling: float = 0.0) -> Self:
        assert self._is_reward_fn_logged, "Reward needs to be logged to zero-sum it"
        self._reward_fn = ZeroSumWrapper(self._reward_fn, team_spirit, opp_scaling)  # noqa, the assertion catches the issue
        return self

    def weight(self, weight: float, propagate_to_logs: bool = True) -> Self:
        assert self._is_reward_fn_logged, "Reward needs to be logged to weight it"
        self._reward_fn = WeightedWrapper(self._reward_fn, weight, propagate_to_logs)
        return self

    def rename(self, name: str) -> Self:
        self._reward_fn = CustomNameWrapper(self._reward_fn, name)
        return self

    def fill_metrics(self) -> Self:
        assert self._is_reward_fn_logged, "Reward needs to be logged to fill its metrics"
        self._reward_fn = FillMetricsWrapper(self._reward_fn)
        return self

    def default_if_none(self, default_value: float = 0.0) -> Self:
        assert self._is_reward_fn_logged, "Reward needs to be logged to default the value"
        self._reward_fn = DefaultIfNoneWrapper(self._reward_fn, default_value)
        return self

    def to_logged(self) -> Self:
        self._reward_fn = RewardFnWrapper(self._reward_fn)
        self._is_reward_fn_logged = True
        return self

    def apply_operation(self, operation: Callable[[float], float] = lambda x: x) -> Self:
        assert self._is_reward_fn_logged, "Reward needs to be logged to apply an operation on it"
        self._reward_fn = ApplyOperationWrapper(self._reward_fn, operation)
        return self

    def debug(self) -> Self:
        assert self._is_reward_fn_logged, "Reward needs to be logged to debug it"
        self._reward_fn = DebugWrapper(self._reward_fn)
        return self
