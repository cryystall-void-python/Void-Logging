from typing import Generic, Dict, Any, List

from rlgym_learn.api import AgentControllerData
from rlgym_learn_algos.logging import DictMetricsLogger, InnerMetricsLoggerConfig, \
    InnerMetricsLoggerAdditionalDerivedConfig, MetricsLoggerConfig

from ..logging_utils import AvgTracker, REWARDS_HEADER


def nest_dict(flat_dict, total_first=True):
    nested = {}
    for flat_key, value in flat_dict.items():
        parts = flat_key.split("/")
        current = nested
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                old_val = current[part]
                current[part] = {}
                if total_first:
                    current[part]["Total"] = old_val
                else:
                    current[part] = {**current[part], "Total": old_val}
            current = current[part]
        last = parts[-1]
        if last in current and isinstance(current[last], dict):
            if total_first:
                # Move 'Total' to first if exists, else insert
                if "Total" not in current[last]:
                    current[last] = {"Total": value, **current[last]}
                else:
                    current[last]["Total"] = value
            else:
                current[last]["Total"] = value
        elif last in current and not isinstance(current[last], dict):
            old_val = current[last]
            current[last] = {}
            if total_first:
                current[last]["Total"] = old_val
                current[last]["Total"] = value
            else:
                current[last] = {**current[last], "Total": value}
        else:
            current[last] = value
    return nested

class RewardLogger(
    DictMetricsLogger[
        None,
        None,
        None
    ],
    Generic[
        InnerMetricsLoggerConfig,
        InnerMetricsLoggerAdditionalDerivedConfig,
        AgentControllerData,
    ]
):
    def __init__(self, inner_metrics_logger: DictMetricsLogger[
            InnerMetricsLoggerConfig,
            InnerMetricsLoggerAdditionalDerivedConfig,
            AgentControllerData,
        ]):
        self.inner_metrics_logger = inner_metrics_logger

        self.agent_metrics = {}
        self.env_metrics = {}

    def get_metrics(self) -> Dict[str, Any]:
        return self.env_metrics | self.agent_metrics

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
        self.inner_metrics_logger.collect_env_metrics(data)
        if hasattr(self.inner_metrics_logger, "env_metrics"):
            inner_metrics_logger_env_metrics = self.inner_metrics_logger.env_metrics
        else:
            inner_metrics_logger_env_metrics = {}

        rewards_metrics = {}

        trackers: Dict[str, AvgTracker] = {}

        for shared_info in data:
            rewards_info: dict[str, dict[str, float]] = shared_info[REWARDS_HEADER]

            for _, agent_reward_data in rewards_info.items():
                for metric, value in agent_reward_data.items():
                    if metric not in trackers.keys():
                        trackers.setdefault(metric, AvgTracker())
                    trackers[metric] += float(value)

        rewards_metrics.setdefault(REWARDS_HEADER, {})

        for metric, tracker in trackers.items():
            rewards_metrics[REWARDS_HEADER].setdefault(
                metric, tracker.get_avg()
            )

        self.env_metrics = rewards_metrics | inner_metrics_logger_env_metrics

    def collect_agent_metrics(self, data: AgentControllerData):
        self.inner_metrics_logger.collect_agent_metrics(data)

        if hasattr(self.inner_metrics_logger, "agent_metrics"):
            self.agent_metrics = self.inner_metrics_logger.agent_metrics

    def validate_config(self, config_obj: Dict[str, Any]) -> MetricsLoggerConfig:
        return self.inner_metrics_logger.validate_config(config_obj)