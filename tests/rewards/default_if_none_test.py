from typing import Any, Dict, Generic, List

from rlgym.api.rlgym import AgentID, StateType

from void_logging.api.rewards.logged_float import Logged
from void_logging.api.rewards.logged_reward import LoggedReward
from void_logging.api.wrappers.default_if_none_wrapper import DefaultIfNoneWrapper
from void_logging.logging_utils import REWARDS_HEADER

from tests.create_env import RLGymUnittestCase, create_env, generate_random_actions


class NoValueReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    """A reward that returns no logs and value"""

    @property
    def name(self) -> str:
        return "No value"

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        return {agent: Logged() for agent in agents}

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class DefaultIfNoneWrapperTestCase(RLGymUnittestCase):
    """Tests of the default if none wrapper"""

    def runTest(self):
        """Method to run all tests"""
        self.test_no_value()
        self.test_no_value_with_one()

    def test_no_value(self):
        """Test with the default parameter of the wrapper"""
        reward_fn = DefaultIfNoneWrapper(NoValueReward())
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]

            # The wrapper doesn't add a metric, it just set the value to the specified default value
            self.assertEqual(len(_reward_log), 0)
            self.assertEqual(rewards[agent], 0)

    def test_no_value_with_one(self):
        """Test with another default value than the default param"""

        reward_fn = DefaultIfNoneWrapper(NoValueReward(), default_value=1)
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]

            # The wrapper doesn't add a metric, it just set the value to the specified default value
            self.assertEqual(len(_reward_log), 0)
            self.assertEqual(rewards[agent], 1)
