from tests.create_env import (
    ConstantReward,
    RLGymUnittestCase,
    create_env,
    generate_random_actions,
)
from void_logging.api.rewards.log import SEPARATOR
from void_logging.api.wrappers.custom_name_wrapper import CustomNameWrapper
from void_logging.logging_utils import REWARDS_HEADER


class CustomNameWrapperTestCase(RLGymUnittestCase):
    """Tests for the custom name wrapper"""

    def runTest(self):
        """Method to run all tests"""
        self.test_custom_name()

    def test_custom_name(self):
        """Tests a reward with a custom name"""

        expected_name = "My custom name"
        reward_fn = CustomNameWrapper(ConstantReward(), name=expected_name)
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 1)
            self.assertEqual(reward_fn.name, expected_name)
            self.assertNotIn(ConstantReward.NAME, _reward_log)
            self.assertEqual(
                _reward_log[expected_name + SEPARATOR + ConstantReward.METRIC], 1
            )
            self.assertEqual(rewards[agent], 1)
