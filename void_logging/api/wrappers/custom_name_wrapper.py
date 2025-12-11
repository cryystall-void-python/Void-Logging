from rlgym.api import RewardFunction

from ..wrappers import LoggedWrapper


class CustomNameWrapper(LoggedWrapper):
    def __init__(self, reward_fn: RewardFunction, name: str):
        super().__init__(reward_fn)
        self._name = name

    @property
    def name(self):
        return self._name
