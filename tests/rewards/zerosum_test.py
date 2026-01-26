from tests.create_env import (
    ConstantReward,
    RLGymUnittestCase,
    create_env,
    generate_random_actions,
)
from void_logging.api.rewards.log import SEPARATOR
from void_logging.api.wrappers.zerosum_wrapper import ZeroSumWrapper
from void_logging.logging_utils import REWARDS_HEADER


class ZeroSumTestCase(RLGymUnittestCase):
    """Tests for the zerosum wrapper"""

    def runTest(self):
        self.test_complete_zerosum()
        self.test_partial_zerosum()
        self.test_no_zerosum()

    def test_complete_zerosum(self):
        """Test for a "full" zerosum, basically 1.0 in team spirit and opp scaling, resulting in a 0 in the final reward in the case of a constant reward"""
        reward_fn = ZeroSumWrapper(ConstantReward(), team_spirit=1.0, opp_scaling=1.0)

        env = create_env(reward_fn)
        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 4)

            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.TEAM_SPIRIT_DISTRIBUTION_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.TEAM_SPIRIT_REWARD_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.OPPONENT_SCALING_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC, _reward_log
            )

            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.TEAM_SPIRIT_DISTRIBUTION_METRIC
                ],
                -1,
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.TEAM_SPIRIT_REWARD_METRIC
                ],
                1,
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.OPPONENT_SCALING_METRIC
                ],
                -1,
            )
            self.assertEqual(
                _reward_log[ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC], 1
            )

            self.assertEqual(rewards[agent], 0)

    def test_partial_zerosum(self):
        """Test for a "partial" zerosum, where opponent scaling is 0.5"""
        reward_fn = ZeroSumWrapper(ConstantReward(), team_spirit=0.5, opp_scaling=0.5)

        env = create_env(reward_fn)
        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 4)

            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.TEAM_SPIRIT_DISTRIBUTION_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.TEAM_SPIRIT_REWARD_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.OPPONENT_SCALING_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC, _reward_log
            )

            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.TEAM_SPIRIT_DISTRIBUTION_METRIC
                ],
                -0.5,
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.TEAM_SPIRIT_REWARD_METRIC
                ],
                0.5,
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.OPPONENT_SCALING_METRIC
                ],
                -0.5,
            )
            self.assertEqual(
                _reward_log[ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC], 1
            )

            self.assertEqual(rewards[agent], 0.5)

    def test_no_zerosum(self):
        """Tests with "no" zerosum, basically an empty wrapper"""
        reward_fn = ZeroSumWrapper(ConstantReward(), team_spirit=0.0, opp_scaling=0.0)

        env = create_env(reward_fn)
        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 4)

            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.TEAM_SPIRIT_DISTRIBUTION_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.TEAM_SPIRIT_REWARD_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ZeroSumWrapper.OPPONENT_SCALING_METRIC,
                _reward_log,
            )
            self.assertIn(
                ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC, _reward_log
            )

            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.TEAM_SPIRIT_DISTRIBUTION_METRIC
                ],
                0,
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.TEAM_SPIRIT_REWARD_METRIC
                ],
                0,
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ZeroSumWrapper.OPPONENT_SCALING_METRIC
                ],
                0,
            )
            self.assertEqual(
                _reward_log[ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC], 1
            )

            self.assertEqual(rewards[agent], 1)
