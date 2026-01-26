from collections.abc import Hashable
import random
from typing import Generic, List, Dict, Any
import unittest

import numpy as np
from rlgym.api import AgentID, StateType
from rlgym.rocket_league.sim import RocketSimEngine

from void_logging.api.rewards import Log
from void_logging.api.rewards.logged_float import Logged
from void_logging.api.rewards.logged_reward import LoggedReward
from void_logging.api.rewards.reward_logger import RewardLogger
from void_logging.rlgym_learn import RewardSharedInfoProvider


class DummyReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    def __init__(self):
        self.i = 0

    @property
    def name(self) -> str:
        return "Dummy reward"

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        rewards = {agent: Logged() for agent in agents}

        self.i += 1

        if self.i % 5 == 0:
            for agent in agents:
                rewards[agent] += Log(metric="Test metric", value=random.randint(1, 3))

                rewards[agent] += Log(metric="Test metric 2", value=2)

        return rewards

    @property
    def metrics(self) -> list[str]:
        return ["Test metric", "Test metric 2"]


def create_env(
    reward_fn: LoggedReward, team_size: int = 3, spawn_opponents: bool = True
):
    from rlgym.api.rlgym import RLGym

    from rlgym.rocket_league.state_mutators.kickoff_mutator import KickoffMutator
    from rlgym.rocket_league.state_mutators.mutator_sequence import MutatorSequence
    from rlgym.rocket_league.state_mutators.fixed_team_size_mutator import (
        FixedTeamSizeMutator,
    )

    from rlgym.rocket_league.obs_builders.default_obs import DefaultObs
    from rlgym.rocket_league.action_parsers.lookup_table_action import LookupTableAction

    return RLGym(
        state_mutator=MutatorSequence(
            FixedTeamSizeMutator(
                blue_size=team_size, orange_size=team_size if spawn_opponents else 0
            ),
            KickoffMutator(),
        ),
        obs_builder=DefaultObs(),
        action_parser=LookupTableAction(),
        reward_fn=RewardLogger(reward_fn),
        transition_engine=RocketSimEngine(),
        shared_info_provider=RewardSharedInfoProvider(),
    )


def generate_random_actions(agents: List[AgentID]):
    return {agent: np.asarray([np.random.randint(0, 90)]) for agent in agents}


class RLGymUnittestCase(unittest.TestCase):
    def check_all_agents_are_in(self, agents: List[Hashable], target_dict: dict):
        for agent in agents:
            self.assertIn(agent, target_dict)


class ConstantReward(LoggedReward[AgentID, StateType], Generic[AgentID, StateType]):
    NAME: str = "Constant reward"
    METRIC: str = "Constant"

    @property
    def name(self) -> str:
        return ConstantReward.NAME

    def __init__(self, reward: float = 1.0) -> None:
        self.reward = reward

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
            rewards[agent] += Log(value=self.reward, metric=ConstantReward.METRIC)

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        pass
