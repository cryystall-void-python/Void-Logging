"""Module for the metric logger"""

from typing import Any, Dict, List

from pydantic import BaseModel
from rlgym_learn.pyany_serde import PyAnySerdeType

from rlgym_learn_logging.logging_utils import (
    METRICS_HEADER,
    PLAYERS_METRICS_HEADER,
    STATE_METRICS_HEADER,
    AvgTracker,
)
from rlgym_learn_logging.rlgym_learn.env_metrics_logger import EnvMetricsLogger


class CustomMetricLoggerModelConfig(BaseModel, extra="forbid"):
    """A class for the metric logger in case i want to add config"""


class CustomMetricLogger(EnvMetricsLogger):
    """A class to log what is inside of shared_info[METRICS_HEADER]"""

    SERDE = PyAnySerdeType.TYPEDDICT(
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

    def __init__(self):
        self.env_metrics = {}

    def get_metrics(self) -> Dict[str, Any]:
        return self.env_metrics

    def collect_env_metrics(self, data: List[Dict[str, Any] | None]):
        metrics = {}

        trackers: Dict[str, AvgTracker] = {}

        # Metrics
        #   Players
        #       Player/Velocity
        #           agent_id_1: 0.1
        #   State
        #       whatever 1: 0.1

        for shared_info in data:
            # None when the env sent no shared info (no shared_info_serde_type)
            if shared_info is None:
                continue
            metrics_info: dict[str, Any] = shared_info[METRICS_HEADER]

            # get, not pop: rlgym-learn keeps these shared infos (and saves
            # them in checkpoints), so they must not be modified here.
            player_metrics: dict[str, dict[str, float]] = metrics_info.get(
                PLAYERS_METRICS_HEADER, {}
            )
            state_metrics: dict[str, int | float] = metrics_info.get(
                STATE_METRICS_HEADER, {}
            )

            for metric, agent_metrics_data in player_metrics.items():
                for value in agent_metrics_data.values():
                    if metric not in trackers:
                        trackers.setdefault(metric, AvgTracker())
                    if value is not None:
                        trackers[metric] += float(value)

            for metric, value in state_metrics.items():
                if metric not in trackers:
                    trackers.setdefault(metric, AvgTracker())
                if value is not None:
                    trackers[metric] += float(value)

        metrics.setdefault(METRICS_HEADER, {})

        for metric, tracker in trackers.items():
            metrics[METRICS_HEADER].setdefault(metric, tracker.get_avg())

        self.env_metrics = metrics

