from typing import Any, Dict, Generic, List

from rlgym.api import AgentID, StateType

from rlgym_learn_logging.api.rewards.log import Log
from rlgym_learn_logging.api.rewards.logged_float import Logged
from rlgym_learn_logging.api.rewards.logged_reward import LoggedReward
from rlgym_learn_logging.logging_utils import REWARDS_HEADER
from tests.create_env import RLGymUnittestCase, create_env, generate_random_actions


class AddTestReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    """A reward that adds 2"""

    @property
    def name(self) -> str:
        return "Add test"

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
            rewards[agent] += Log(value=2, metric="Add")

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class SubtractTestReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    """A reward that subtracts 2"""

    @property
    def name(self) -> str:
        return "Subtract test"

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
            rewards[agent] -= Log(value=2, metric="Subtract")

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class MultiplyTestReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    """A reward that multiplies 2 by 3"""

    @property
    def name(self) -> str:
        return "Multiply test"

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
            rewards[agent] += Log(value=2, metric="Add")

            rewards[agent] *= Log(value=3, metric="Multiply")

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class DivideTestReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    """A reward that divides 6 by 3"""

    @property
    def name(self) -> str:
        return "Divide test"

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
            rewards[agent] += Log(value=6, metric="Add")

            rewards[agent] /= Log(value=3, metric="Divide")

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass


class OperationsTestCase(RLGymUnittestCase):
    """Tests for all the possible operations for the Log object"""

    def runTest(self):
        """Method to run all tests"""
        self.test_add()
        self.test_subtract()
        self.test_multiply()
        self.test_divide()

    def test_add(self):
        """Test for the addition of Log"""

        reward_fn = AddTestReward()
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 1)
            self.assertEqual(_reward_log["Add test/Add"], 2)
            self.assertEqual(rewards[agent], 2)

    def test_subtract(self):
        """Test for the subtraction of Log"""

        reward_fn = SubtractTestReward()
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 1)
            self.assertEqual(_reward_log["Subtract test/Subtract"], -2)
            self.assertEqual(rewards[agent], -2)

    def test_multiply(self):
        """Test for the multiplication of Log"""

        reward_fn = MultiplyTestReward()
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 2)
            self.assertEqual(_reward_log["Multiply test/Multiply"], 4)

            self.assertEqual(rewards[agent], 6)

    def test_divide(self):
        """Test for the division of Log"""

        reward_fn = DivideTestReward()
        env = create_env(reward_fn)

        env.reset()

        _, rewards, _, _ = env.step(generate_random_actions(env.agents))

        for agent in env.agents:
            _reward_log: dict = env.shared_info[REWARDS_HEADER][agent]
            self.assertEqual(len(_reward_log), 2)
            self.assertAlmostEqual(_reward_log["Divide test/Divide"], -4.0)

            self.assertEqual(rewards[agent], 2)
