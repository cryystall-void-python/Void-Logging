from typing import Dict, Any, List

from pydantic import BaseModel
from rlgym_learn import PyAnySerdeType
from rlgym_learn_algos.logging import MetricsLoggerConfig
from rlgym_learn_algos.logging.dict_metrics_logger import DictMetricsLogger

from void_logging.logging_utils import (
    AvgTracker,
    METRICS_HEADER,
    PLAYERS_METRICS_HEADER,
    STATE_METRICS_HEADER,
)


def get_serde_type(value: Any) -> int:
    if isinstance(value, int):
        return 0
    elif isinstance(value, float):
        return 1


custom_metrics_serde = lambda: PyAnySerdeType.TYPEDDICT(
    key_serde_type_dict={
        PLAYERS_METRICS_HEADER: PyAnySerdeType.DICT(
            keys_serde_type=PyAnySerdeType.STRING(),
            values_serde_type=PyAnySerdeType.DICT(
                keys_serde_type=PyAnySerdeType.STRING(),
                values_serde_type=PyAnySerdeType.OPTION(PyAnySerdeType.FLOAT()),
            ),
        ),
        STATE_METRICS_HEADER: PyAnySerdeType.DICT(
            keys_serde_type=PyAnySerdeType.STRING(),
            values_serde_type=PyAnySerdeType.OPTION(PyAnySerdeType.FLOAT()),
        ),
    }
)


class CustomMetricLoggerModelConfig(BaseModel, extra="forbid"):
    pass


class CustomMetricLogger(DictMetricsLogger[CustomMetricLoggerModelConfig, None, None]):
    def __init__(self):
        self.env_metrics = {}

    def get_metrics(self) -> Dict[str, Any]:
        return self.env_metrics

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
        metrics = {}

        trackers: Dict[str, AvgTracker] = {}

        # Metrics
        #   Players
        #       Player/Velocity
        #           agent_id_1: 0.1
        #   State
        #       whatever 1: 0.1

        for shared_info in data:
            metrics_info: dict[str, Any] = shared_info[METRICS_HEADER]

            player_metrics: dict[str, dict[str, float]] = metrics_info.pop(
                PLAYERS_METRICS_HEADER, {}
            )
            state_metrics: dict[str, int | float] = metrics_info.pop(
                STATE_METRICS_HEADER, {}
            )

            for metric, agent_metrics_data in player_metrics.items():
                for agent, value in agent_metrics_data.items():
                    if metric not in trackers.keys():
                        trackers.setdefault(metric, AvgTracker())
                    if value is not None:
                        trackers[metric] += float(value)

            for metric, value in state_metrics.items():
                if metric not in trackers.keys():
                    trackers.setdefault(metric, AvgTracker())
                if value is not None:
                    trackers[metric] += float(value)

        metrics.setdefault(METRICS_HEADER, {})

        for metric, tracker in trackers.items():
            metrics[METRICS_HEADER].setdefault(metric, tracker.get_avg())

        self.env_metrics = metrics

    def validate_config(self, config_obj: Dict[str, Any]) -> MetricsLoggerConfig:
        return CustomMetricLoggerModelConfig.model_validate(config_obj)
