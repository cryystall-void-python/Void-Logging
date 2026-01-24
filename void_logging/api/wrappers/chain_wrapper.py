"""Module for the chain wrapper"""

from typing import Self, Callable

from void_logging.api.wrappers.apply_operation_wrapper import ApplyOperationWrapper
from void_logging.api.wrappers.custom_name_wrapper import CustomNameWrapper
from void_logging.api.wrappers.debug_wrapper import DebugWrapper
from void_logging.api.wrappers.default_if_none_wrapper import DefaultIfNoneWrapper
from void_logging.api.wrappers.fill_metrics_wrapper import FillMetricsWrapper
from void_logging.api.wrappers.reward_fn_wrapper import RewardFnWrapper
from void_logging.api.wrappers.weighted_wrapper import WeightedWrapper
from void_logging.api.wrappers.wrapper import LoggedWrapper
from void_logging.api.wrappers.zerosum_wrapper import ZeroSumWrapper


class ChainWrapper(LoggedWrapper):
    """
    A wrapper to allow the use of chain functions
    """

    def zero_sum(self, team_spirit: float = 0.0, opp_scaling: float = 0.0) -> Self:
        """Transform a reward to a zerosum reward

        :param team_spirit: The team spirit distribution amount
            (the bigger it is, the more team score will matter).
            Defaults to 0.0.
        :param opp_scaling: The opponent scaling amount
            (the bigger it is, the more "adversity" it'll create (as well as noise)).
            Defaults to 0.0.

        :return: itself (Self): Itself
        """
        assert self._is_reward_fn_logged, "Reward needs to be logged to zero-sum it"
        self._reward_fn = ZeroSumWrapper(self._reward_fn, team_spirit, opp_scaling)
        return self

    def weight(self, weight: float, propagate_to_logs: bool = True) -> Self:
        """Transform a reward to a weighted reward

        :param weight: The weight you need to apply. Defaults to 1.0.
        :param propagate_to_logs: Whether you want to see the weighted metrics
            or another field called "Weight" that shows the impact
            of the weight on the final value.
            Defaults to True.

        :return: itself (Self): Itself
        """
        assert self._is_reward_fn_logged, "Reward needs to be logged to weight it"
        self._reward_fn = WeightedWrapper(self._reward_fn, weight, propagate_to_logs)
        return self

    def rename(self, name: str) -> Self:
        """Renames the reward function

        :param name: The new name

        :return: itself (Self): Itself
        """
        self._reward_fn = CustomNameWrapper(self._reward_fn, name)
        return self

    def fill_metrics(self) -> Self:
        """Fills the metrics of the reward using the self.metrics attribute of said reward

        :return: itself (Self): Itself
        """
        assert self._is_reward_fn_logged, (
            "Reward needs to be logged to fill its metrics"
        )
        self._reward_fn = FillMetricsWrapper(self._reward_fn)
        return self

    def default_if_none(self, default_value: float = 0.0) -> Self:
        """Sets a default value in case None is received

        :param default_value: Said default value. Defaults to 0.0.

        :return: itself (Self): Itself
        """
        assert self._is_reward_fn_logged, (
            "Reward needs to be logged to default the value"
        )
        self._reward_fn = DefaultIfNoneWrapper(self._reward_fn, default_value)
        return self

    def to_logged(self) -> Self:
        """Transforms a "classic" reward into a logged one

        :return: itself (Self): Itself
        """
        self._reward_fn = RewardFnWrapper(self._reward_fn)
        self._is_reward_fn_logged = True
        return self

    def apply_operation(
        self, operation: Callable[[float], float] = lambda x: x
    ) -> Self:
        """Applies an operation to the value of the reward

        :param operation: The operation to apply. Defaults to lambda x: x.

        :return: itself (Self): Itself
        """
        assert self._is_reward_fn_logged, (
            "Reward needs to be logged to apply an operation on it"
        )
        self._reward_fn = ApplyOperationWrapper(self._reward_fn, operation)
        return self

    def debug(self) -> Self:
        """Debugs the reward (WIP)

        :return: itself (Self): Itself
        """
        assert self._is_reward_fn_logged, "Reward needs to be logged to debug it"
        self._reward_fn = DebugWrapper(self._reward_fn)
        return self
