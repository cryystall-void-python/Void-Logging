from tests.create_env import (
    ConstantReward,
    RLGymUnittestCase,
    create_env,
    generate_random_actions,
)
from void_logging.api.rewards.log import SEPARATOR
from void_logging.api.rewards.logged_combined_reward import LoggedCombinedReward
from void_logging.logging_utils import REWARDS_HEADER


class LoggedCombinedRewardTestCase(RLGymUnittestCase):
    """Tests of the logged combined reward"""

    def runTest(self):
        """Method to run all tests"""
        self.test_one_reward()
        self.test_multiple_rewards()

    def test_one_reward(self):
        """Tests wth only one reward"""

        reward_fn = LoggedCombinedReward(ConstantReward())

        env = create_env(reward_fn)
        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 2)
            self.assertEqual(rewards[agent], 1.0)

            self.assertIn(
                LoggedCombinedReward.NAME
                + SEPARATOR
                + ConstantReward.NAME
                + SEPARATOR
                + ConstantReward.METRIC,
                _reward_log,
            )
            self.assertIn(
                LoggedCombinedReward.NAME
                + SEPARATOR
                + ConstantReward.NAME
                + SEPARATOR
                + ConstantReward.METRIC,
                _reward_log,
            )

    def test_multiple_rewards(self):
        """Test with multiple rewards"""

        reward_fn = LoggedCombinedReward(
            ConstantReward(),
            ConstantReward(),
            ConstantReward(),
            ConstantReward(),
            ConstantReward(),
            ConstantReward(),
        )

        env = create_env(reward_fn)
        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 2)
            self.assertEqual(rewards[agent], 6.0)

            self.assertIn(
                LoggedCombinedReward.NAME
                + SEPARATOR
                + ConstantReward.NAME
                + SEPARATOR
                + ConstantReward.METRIC,
                _reward_log,
            )
            self.assertIn(
                LoggedCombinedReward.NAME
                + SEPARATOR
                + ConstantReward.NAME
                + SEPARATOR
                + ConstantReward.METRIC,
                _reward_log,
            )
