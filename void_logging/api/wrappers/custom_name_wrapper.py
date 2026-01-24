"""Module for the custom name wrapper"""

from rlgym.api import RewardFunction

from ..wrappers import LoggedWrapper


class CustomNameWrapper(LoggedWrapper):
    """A wrapper to change the name of a reward"""

    def __init__(self, reward_fn: RewardFunction, name: str):
        """A wrapper to change the name of a reward

        :param reward_fn: The reward function to work with
        :param name: The new name
        """
        super().__init__(reward_fn)
        self._name = name

    @property
    def name(self):
        return self._name
