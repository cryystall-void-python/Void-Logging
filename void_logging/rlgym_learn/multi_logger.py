"""Module for the multi logger"""

from dataclasses import dataclass
from typing import Any, Dict, Generic, List

from pydantic import BaseModel, ValidationError
from rlgym_learn.api.typing import AgentControllerData
from rlgym_learn_algos.logging import (
    DictMetricsLogger,
    InnerMetricsLoggerAdditionalDerivedConfig,
    InnerMetricsLoggerConfig,
)
from rlgym_learn_algos.logging.metrics_logger import DerivedMetricsLoggerConfig


class MultiLoggerConfigModel(BaseModel, Generic[InnerMetricsLoggerConfig]):
    inner_metrics_logger_config: List[InnerMetricsLoggerConfig | None] = []


@dataclass
class MultiLoggerAdditionalDerivedConfig(
    Generic[InnerMetricsLoggerAdditionalDerivedConfig]
):
    inner_metrics_logger_additional_derived_config: List[
        InnerMetricsLoggerAdditionalDerivedConfig | None
    ] = []


class MultiLogger(
    DictMetricsLogger[
        MultiLoggerConfigModel[InnerMetricsLoggerConfig],
        MultiLoggerAdditionalDerivedConfig[InnerMetricsLoggerAdditionalDerivedConfig],
        AgentControllerData,
    ],
    Generic[
        InnerMetricsLoggerConfig,
        InnerMetricsLoggerAdditionalDerivedConfig,
        AgentControllerData,
    ],
):
    """A class to log multiple loggers"""

    def __init__(self, *inner_metrics_loggers: DictMetricsLogger):
        self.inner_metrics_loggers = inner_metrics_loggers
        self.env_metrics = {}
        self.agent_metrics = {}

    def validate_config(self, config_obj: Dict[str, Any]) -> MultiLoggerConfigModel:
        _base_config = MultiLoggerConfigModel.model_validate(config_obj)

        # This should never occur
        if "inner_metrics_logger_config" not in config_obj:
            raise ValidationError(
                "Expected 'inner_metrics_logger_config' in config object"
            )

        try:
            _len = len(config_obj["inner_metrics_logger_config"])

            if _len != len(self.inner_metrics_loggers):
                raise ValidationError(
                    f"You gave {_len} config objects for {len(self.inner_metrics_loggers)}. Please provide an equal number for both. If one of the metric loggers used doesn't need any config, you can use None as a filler"
                )
        except TypeError as e:
            raise TypeError(
                f"The config you gave to the multi logger has no length. Config type: {type(config_obj['inner_metrics_logger_config'])}"
            ) from e

        for _idx, inner_metric_logger in enumerate(self.inner_metrics_loggers):
            _config = inner_metric_logger.validate_config(
                config_obj["inner_metrics_logger_config"][_idx]
            )

            _base_config.inner_metrics_logger_config[_idx] = _config

        return _base_config

    def load(
        self,
        config: DerivedMetricsLoggerConfig[
            MultiLoggerConfigModel[InnerMetricsLoggerConfig],
            MultiLoggerAdditionalDerivedConfig[
                InnerMetricsLoggerAdditionalDerivedConfig
            ],
        ],
    ):
        self.config = config

        for _idx, inner_metric_logger in enumerate(self.inner_metrics_loggers):
            _inner_derived_config = config.additional_derived_config.inner_metrics_logger_additional_derived_config[
                _idx
            ]
            _inner_config = config.metrics_logger_config.inner_metrics_logger_config[
                _idx
            ]

            if _inner_config is not None and _inner_derived_config is not None:
                inner_metric_logger.load(
                    DerivedMetricsLoggerConfig(
                        metrics_logger_config=_inner_config,
                        additional_derived_config=_inner_derived_config,
                        checkpoint_load_folder=config.checkpoint_load_folder,
                        agent_controller_name=config.agent_controller_name,
                    )
                )

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
        for inner_metric_logger in self.inner_metrics_loggers:
            inner_metric_logger.collect_env_metrics(data)

    def collect_agent_metrics(self, data: AgentControllerData):
        for inner_metric_logger in self.inner_metrics_loggers:
            inner_metric_logger.collect_agent_metrics(data)

    def get_metrics(self) -> Dict[str, Any]:
        _metrics = {}

        for inner_metric_logger in self.inner_metrics_loggers:
            _metrics = _metrics | inner_metric_logger.get_metrics()

        return _metrics

    def report_metrics(self):
        for inner_metric_logger in self.inner_metrics_loggers:
            inner_metric_logger.report_metrics()
