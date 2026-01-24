"""Module for the base Logged reward class"""

from abc import abstractmethod
from typing import Generic

from rlgym.api import AgentID, StateType
from rlgym.api.rlgym import RewardFunction

from .logged_float import Logged


class LoggedReward(
    Generic[AgentID, StateType], RewardFunction[AgentID, StateType, Logged]
):
    """The very base class for the logging system, can hold a name and metric names"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the reward function
        that will appear in the logging
        (unless using a specific wrapper)

:return: name (str): Name of the reward function
        """

    @property
    def metrics(self) -> list[str]:
        """
        All the metrics that will appear in the reward

        THIS IS NOT AUTOMATICALLY FILLED, YOU HAVE TO FILL IT IF YOU WANT TO USE IT
        :return: An object that holds the reward
        """
        return []
