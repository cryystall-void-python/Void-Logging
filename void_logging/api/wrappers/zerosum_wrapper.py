from typing import List, Dict, Any

from rlgym.api import AgentID
from rlgym.rocket_league.api import GameState

from ..rewards import Logged, Log, LoggedReward
from ..wrappers import LoggedWrapper


class ZeroSumWrapper(LoggedWrapper):
    TEAM_SPIRIT_DISTRIBUTION_METRIC: str = "Team spirit distribution"
    TEAM_SPIRIT_REWARD_METRIC: str = "Team spirit reward"
    OPPONENT_SCALING_METRIC: str = "Opponent scaling"

    def __init__(
        self,
        reward_fn: LoggedReward,
        team_spirit: float = 0.0,
        opp_scaling: float = 0.0,
    ):
        """
        A wrapper to zero-sum a reward
        :param reward_fn: The reward function to zero-sum
        :param team_spirit: The team spirit distribution amount (the bigger it is, the more team score will matter)
        :param opp_scaling: The opponent scaling amount (the bigger it is, the more "adversity" it'll create (as well as noise))
        """
        super().__init__(reward_fn)

        self._team_spirit = team_spirit
        self._opp_scaling = opp_scaling

    def get_rewards(
        self,
        agents: List[AgentID],
        state: GameState,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        rewards = super().get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )

        _blue_rewards = []
        _orange_rewards = []

        for agent in agents:
            assert rewards[agent].get_value() is not None, (
                "ZeroSum expects a value that is not None, use DefaultIfNoneWrapper to fix that"
            )

            if state.cars[agent].is_blue:
                _blue_rewards.append(rewards[agent].get_value())
            else:
                _orange_rewards.append(rewards[agent].get_value())

        _mean_blue_rw = (
            sum(_blue_rewards) / len(_blue_rewards) if len(_blue_rewards) > 0 else 0
        )
        _mean_orange_rw = (
            sum(_orange_rewards) / len(_orange_rewards)
            if len(_orange_rewards) > 0
            else 0
        )

        for agent in agents:
            _car = state.cars[agent]

            # Team spirit distribution
            rewards[agent] *= Log(
                value=1 - self._team_spirit, metric=self.TEAM_SPIRIT_DISTRIBUTION_METRIC
            )

            if _car.is_blue:
                # Team specific spirit
                rewards[agent] += Log(
                    value=_mean_blue_rw * self._team_spirit,
                    metric=self.TEAM_SPIRIT_REWARD_METRIC,
                )
                rewards[agent] -= Log(
                    value=_mean_orange_rw * self._opp_scaling,
                    metric=self.OPPONENT_SCALING_METRIC,
                )
            else:
                # Team specific spirit
                rewards[agent] += Log(
                    value=_mean_orange_rw * self._team_spirit,
                    metric=self.TEAM_SPIRIT_REWARD_METRIC,
                )
                rewards[agent] -= Log(
                    value=_mean_blue_rw * self._opp_scaling,
                    metric=self.OPPONENT_SCALING_METRIC,
                )

        return rewards

    @property
    def metrics(self) -> list[str]:
        return super().metrics + [
            self.TEAM_SPIRIT_DISTRIBUTION_METRIC,
            self.TEAM_SPIRIT_REWARD_METRIC,
            self.OPPONENT_SCALING_METRIC,
        ]
