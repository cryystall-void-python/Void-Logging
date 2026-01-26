from typing import Any, Dict, Generic, List
from rlgym.api import AgentID, StateType, RewardFunction

from tests.create_env import RLGymUnittestCase, create_env, generate_random_actions
from void_logging.api.rewards.log import SEPARATOR
from void_logging.api.wrappers.reward_fn_wrapper import RewardFnWrapper
from void_logging.logging_utils import REWARDS_HEADER


class BaseReward(
    RewardFunction[AgentID, StateType, float], Generic[AgentID, StateType]
):
    """A reward function that returns 2"""

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, float]:
        return {agent: 2 for agent in agents}

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class RewardFnWrapperTestCase(RLGymUnittestCase):
    """Tests for the reward function wrapper"""

    def runTest(self):
        """Method to run all tests"""
        self.test_to_logged()

    def test_to_logged(self):
        """Test to convert a reward to a logged one"""
        reward_fn = RewardFnWrapper(BaseReward())
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 1)
            self.assertIn(
                "Base" + SEPARATOR + RewardFnWrapper.REWARD_VALUE_METRIC, _reward_log
            )
            self.assertEqual(
                _reward_log["Base" + SEPARATOR + RewardFnWrapper.REWARD_VALUE_METRIC], 2
            )

            self.assertEqual(rewards[agent], 2)
