from typing import Any, Dict, Generic, List

from rlgym.api import AgentID, StateType

from rlgym_learn_logging.api.rewards.log import SEPARATOR, Log
from rlgym_learn_logging.api.rewards.logged_float import Logged
from rlgym_learn_logging.api.rewards.logged_reward import LoggedReward
from rlgym_learn_logging.api.wrappers.fill_metrics_wrapper import FillMetricsWrapper
from rlgym_learn_logging.logging_utils import REWARDS_HEADER
from tests.create_env import RLGymUnittestCase, create_env, generate_random_actions


class MultipleMetricsReward(
    LoggedReward[AgentID, StateType], Generic[AgentID, StateType]
):
    """A reward that gives +2 with unused metrics"""

    NAME: str = "Multiple metrics"

    DEFAULT_VALUE = "Default value"
    METRIC_1 = "Metric 1"
    METRIC_2 = "Metric 2"

    @property
    def name(self) -> str:
        return MultipleMetricsReward.NAME

    @property
    def metrics(self) -> list[str]:
        return [
            MultipleMetricsReward.DEFAULT_VALUE,
            MultipleMetricsReward.METRIC_1,
            MultipleMetricsReward.METRIC_2,
        ]

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        rewards = {agent: Logged() for agent in agents}

        for agent in agents:
            rewards[agent] += Log(value=2, metric=MultipleMetricsReward.DEFAULT_VALUE)

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class FillMetricsWrapperTestCase(RLGymUnittestCase):
    """Tests for the fill metrics wrapper"""

    def runTest(self):
        """Method to run all tests"""
        self.test_fill_metrics()

    def test_fill_metrics(self):
        """Test to see if the metrics are filled with the
        right value and doesn't overwrite any existing value"""
        reward_fn = FillMetricsWrapper(MultipleMetricsReward(), 0)
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 3)
            self.assertIn(
                MultipleMetricsReward.NAME
                + SEPARATOR
                + MultipleMetricsReward.DEFAULT_VALUE,
                _reward_log,
            )
            self.assertIn(
                MultipleMetricsReward.NAME + SEPARATOR + MultipleMetricsReward.METRIC_1,
                _reward_log,
            )
            self.assertIn(
                MultipleMetricsReward.NAME + SEPARATOR + MultipleMetricsReward.METRIC_2,
                _reward_log,
            )

            self.assertEqual(
                _reward_log[
                    MultipleMetricsReward.NAME
                    + SEPARATOR
                    + MultipleMetricsReward.DEFAULT_VALUE
                ],
                2,
            )
            self.assertEqual(
                _reward_log[
                    MultipleMetricsReward.NAME
                    + SEPARATOR
                    + MultipleMetricsReward.METRIC_1
                ],
                0,
            )
            self.assertEqual(
                _reward_log[
                    MultipleMetricsReward.NAME
                    + SEPARATOR
                    + MultipleMetricsReward.METRIC_2
                ],
                0,
            )

            self.assertEqual(rewards[agent], 2)
