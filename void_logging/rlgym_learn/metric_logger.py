from typing import Dict, Any, List

from pydantic import BaseModel
from rlgym_learn import PyAnySerdeType
from rlgym_learn_algos.logging import MetricsLoggerConfig
from rlgym_learn_algos.logging.dict_metrics_logger import DictMetricsLogger

from void_logging.logging_utils import AvgTracker, METRICS_HEADER

def get_serde_type(value: Any) -> int:
    if isinstance(value, float):
        return 0
    elif isinstance(value, int):
        return 1

type CustomMetricSerde = PyAnySerdeType.DICT(
    keys_serde_type=PyAnySerdeType.STRING,
    values_serde_type=PyAnySerdeType.UNION(
        option_serde_types=[PyAnySerdeType.FLOAT, PyAnySerdeType.INT],
        option_choice_fn=get_serde_type
    )
)

class CustomMetricLoggerModelConfig(BaseModel, extra="forbid"):
    pass


class CustomMetricLogger(DictMetricsLogger[
        CustomMetricLoggerModelConfig,
        None,
        None
    ]):
    def __init__(self):
        self.env_metrics = {}

    def get_metrics(self) -> Dict[str, Any]:
        return self.env_metrics

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
        metrics = {}

        trackers: Dict[str, AvgTracker] = {}

        for shared_info in data:
            rewards_info: dict[str, dict[str, float]] = shared_info[METRICS_HEADER]

            for _, agent_reward_data in rewards_info.items():
                for metric, value in agent_reward_data.items():
                    if metric not in trackers.keys():
                        trackers.setdefault(metric, AvgTracker())
                    trackers[metric] += float(value)

        metrics.setdefault(METRICS_HEADER, {})

        for metric, tracker in trackers.items():
            metrics[METRICS_HEADER].setdefault(
                metric, tracker.get_avg()
            )

        self.env_metrics = metrics

    def validate_config(self, config_obj: Dict[str, Any]) -> MetricsLoggerConfig:
        return CustomMetricLoggerModelConfig.model_validate(config_obj)