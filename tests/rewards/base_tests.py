from tests.create_env import DummyReward, RLGymUnittestCase, create_env
from void_logging.logging_utils import REWARDS_HEADER


class BaseTestsCase(RLGymUnittestCase):
    """Tests for the setup of the logged reward"""

    def runTest(self):
        """Method to run all tests"""
        self.test_presence()

    def test_presence(self):
        """Tests whether the shared info has the correct information to begin with"""
        reward_fn = DummyReward()
        env = create_env(reward_fn)

        env.reset()

        self.assertIn(REWARDS_HEADER, env.shared_info)
        self.check_all_agents_are_in(env.agents, env.shared_info[REWARDS_HEADER])
