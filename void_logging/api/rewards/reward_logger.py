from typing import Generic, Any, List, Dict

from rlgym.api import AgentID, RewardType, StateType, RewardFunction

from .logged_float import Logged
from .log import SEPARATOR
from .logged_reward import LoggedReward
from ...logging_utils import REWARDS_HEADER


class RewardLogger(
    Generic[AgentID, StateType, RewardType],
    RewardFunction[AgentID, StateType, RewardType],
):
    def __init__(
        self,
        logged_reward: LoggedReward[AgentID, StateType],
        prefix_with_reward_name: bool = True,
    ):
        self._logged_reward = logged_reward
        self._prefix_with_reward_name = prefix_with_reward_name

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, float]:
        rewards = {agent: 0.0 for agent in agents}
        _inner_rewards = self._logged_reward.get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )

        for agent in agents:
            rewards[agent] = _inner_rewards[agent].get_value()

        self.log(_inner_rewards, shared_info)

        return rewards

    def reset(
        self,
        agents: List[AgentID],
        initial_state: StateType,
        shared_info: Dict[str, Any],
    ) -> None:
        self._logged_reward.reset(agents, initial_state, shared_info)

    def log(self, logs: dict[AgentID, Logged], shared_info: dict[str, Any]) -> None:
        for agent_id, _logs in logs.items():
            _logs.sanitize()
            _copy_logs = _logs.get_logs().copy()

            if self._prefix_with_reward_name:
                for _metric, _value in _logs.get_logs().items():
                    if len(_metric.strip()) == 0:
                        _to_log_metric = self._logged_reward.name
                    else:
                        _to_log_metric = self._logged_reward.name + SEPARATOR + _metric

                    _copy_logs[_to_log_metric] = _copy_logs.pop(_metric)

            shared_info[REWARDS_HEADER][agent_id] = _copy_logs
