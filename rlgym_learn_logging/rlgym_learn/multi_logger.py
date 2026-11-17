"""Module for the multi logger"""

from dataclasses import dataclass
from dataclasses import field as data_field
from typing import Any, Dict, Generic, List

from pydantic import BaseModel, Field, ValidationError
from rlgym_learn.api.typing import AgentControllerData
from rlgym_learn_algos.logging import (
    DictMetricsLogger,
    InnerMetricsLoggerAdditionalDerivedConfig,
    InnerMetricsLoggerConfig,
)
from rlgym_learn_algos.logging.metrics_logger import (
    DerivedMetricsLoggerConfig,
    MetricsLoggerConfig,
)


class MultiLoggerConfigModel(BaseModel, Generic[MetricsLoggerConfig]):
    inner_metrics_logger_config: List[MetricsLoggerConfig | None] = Field(
        default_factory=list
    )


@dataclass
class MultiLoggerAdditionalDerivedConfig(
    Generic[InnerMetricsLoggerAdditionalDerivedConfig]
):
    inner_metrics_logger_additional_derived_config: List[
        InnerMetricsLoggerAdditionalDerivedConfig | None
    ] = data_field(default_factory=list)


class MultiLogger(
    DictMetricsLogger[
        Any, MultiLoggerConfigModel, Any, Any, Any, Any, Any, Any, Any, Any
    ]
):
    """A class to log multiple loggers"""

    def __init__(self, *inner_metrics_loggers: DictMetricsLogger):
        self.inner_metrics_loggers = inner_metrics_loggers

    @property
    def config_model(self) -> type[MultiLoggerConfigModel]:
        return MultiLoggerConfigModel

    def load(self, config: DerivedMetricsLoggerConfig) -> None:
        self.config = config
        inner_configs = (
            config.metrics_logger_config.inner_metrics_logger_config
            if config.metrics_logger_config is not None
            else []
        ) or [None] * len(self.inner_metrics_loggers)
        for idx, (logger, inner_config) in enumerate(
            zip(self.inner_metrics_loggers, inner_configs)
        ):
            logger.load(
                DerivedMetricsLoggerConfig(
                    agent_controller_name=config.agent_controller_name,
                    derived_agent_controller_config=config.derived_agent_controller_config,
                    metrics_logger_config=inner_config,
                    checkpoint_load_folder=None
                    if config.checkpoint_load_folder is None
                    else os.path.join(
                        config.checkpoint_load_folder, INNER_LOGGER_FOLDER.format(idx)
                    ),
                )
            )

    def save_checkpoint(self, folder_path: str | PathLike[str]) -> None:
        for idx, logger in enumerate(self.inner_metrics_loggers):
            inner_folder = os.path.join(folder_path, INNER_LOGGER_FOLDER.format(idx))
            os.makedirs(inner_folder, exist_ok=True)
            logger.save_checkpoint(inner_folder)

    def collect_env_metrics(self, data: List[Dict[str, Any] | None]):
        for inner_metric_logger in self.inner_metrics_loggers:
            inner_metric_logger.collect_env_metrics(data)

    def collect_agent_metrics(self, data: Any):
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
