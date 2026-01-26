from tests.create_env import (
    ConstantReward,
    RLGymUnittestCase,
    create_env,
    generate_random_actions,
)
from void_logging.api.rewards.log import SEPARATOR
from void_logging.api.wrappers.apply_operation_wrapper import ApplyOperationWrapper
from void_logging.logging_utils import REWARDS_HEADER


class ApplyOperationWrapperTestCase(RLGymUnittestCase):
    """Tests for the apply operation wrapper"""

    def runTest(self):
        """Method that runs all tests"""
        self.test_apply_random_operation()

    def test_apply_random_operation(self):
        """Test whether applying an operation work"""

        reward_fn = ApplyOperationWrapper(ConstantReward(), lambda x: x + 1)
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 2)

            self.assertIn(
                ConstantReward.NAME
                + SEPARATOR
                + ApplyOperationWrapper.USER_OPERATION_METRIC,
                _reward_log,
            )

            self.assertEqual(
                _reward_log[ConstantReward.NAME + SEPARATOR + ConstantReward.METRIC], 1
            )
            self.assertEqual(
                _reward_log[
                    ConstantReward.NAME
                    + SEPARATOR
                    + ApplyOperationWrapper.USER_OPERATION_METRIC
                ],
                1,
            )
            self.assertEqual(rewards[agent], 2)
