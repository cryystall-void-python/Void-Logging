from abc import abstractmethod
from typing import Generic, Any, TypeVar

from rlgym.api import AgentID, StateType
from rlgym.api.rlgym import RewardFunction

from .logged_float import Logged


class LoggedReward(
    Generic[AgentID, StateType], RewardFunction[AgentID, StateType, Logged]
):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def metrics(self) -> list[str]:
        """
        All the metrics that will appear in the reward

        THIS IS NOT AUTOMATICALLY FILLED, YOU HAVE TO FILL IT IF YOU WANT TO USE IT
        :return: An object that holds the reward
        """
        return []
