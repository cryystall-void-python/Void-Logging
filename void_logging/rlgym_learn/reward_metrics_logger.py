from typing import Generic, Dict, Any, List

from pydantic import BaseModel
from rlgym_learn import PyAnySerdeType
from rlgym_learn.api import AgentControllerData
from rlgym_learn_algos.logging import (
    DictMetricsLogger,
    InnerMetricsLoggerConfig,
    InnerMetricsLoggerAdditionalDerivedConfig,
    MetricsLoggerConfig,
)

from ..logging_utils import AvgTracker, REWARDS_HEADER


class RewardMetricLoggerConfigModel(BaseModel, extra="forbid"):
    pass


reward_metric_logger_serde = PyAnySerdeType.DICT(
    keys_serde_type=PyAnySerdeType.STRING(),
    values_serde_type=PyAnySerdeType.DICT(
        keys_serde_type=PyAnySerdeType.STRING(),
        values_serde_type=PyAnySerdeType.FLOAT(),
    ),
)


class RewardMetricsLogger(DictMetricsLogger[RewardMetricLoggerConfigModel, None, None]):
    def __init__(self):
        self.env_metrics = {}

    def get_metrics(self) -> Dict[str, Any]:
        return self.env_metrics

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
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
            rewards_metrics[REWARDS_HEADER].setdefault(metric, tracker.get_avg())

        self.env_metrics = rewards_metrics

    def validate_config(self, config_obj: Dict[str, Any]) -> MetricsLoggerConfig:
        return RewardMetricLoggerConfigModel.model_validate(config_obj)
