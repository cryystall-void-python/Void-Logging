from dataclasses import dataclass
from typing import Generic, Dict, Any, List

from pydantic import BaseModel
from rlgym_learn.api import AgentControllerData
from rlgym_learn_algos.logging import InnerMetricsLoggerConfig, \
    InnerMetricsLoggerAdditionalDerivedConfig, DictMetricsLogger, MetricsLoggerConfig

from ..logging_utils import print_metrics


class MultiLoggerConfigModel(BaseModel):
    pass

@dataclass
class MultiLoggerAdditionalDerivedConfig(
    Generic[InnerMetricsLoggerConfig, InnerMetricsLoggerAdditionalDerivedConfig]
):
    inner_metrics_logger_config: InnerMetricsLoggerConfig = None
    inner_metrics_logger_additional_derived_config: (
        InnerMetricsLoggerAdditionalDerivedConfig
    ) = None

class MultiLogger(
    DictMetricsLogger[
        MultiLoggerConfigModel,
        MultiLoggerAdditionalDerivedConfig[
            InnerMetricsLoggerConfig, InnerMetricsLoggerAdditionalDerivedConfig
        ],
        AgentControllerData,
    ],
    Generic[
        InnerMetricsLoggerConfig,
        InnerMetricsLoggerAdditionalDerivedConfig,
        AgentControllerData,
    ],
):
    def __init__(
        self,
        *inner_metrics_loggers: DictMetricsLogger
    ):
        self.inner_metrics_loggers = inner_metrics_loggers
        self.env_metrics = {}
        self.agent_metrics = {}

    def validate_config(self, config_obj: Dict[str, Any]) -> MetricsLoggerConfig:
        return MultiLoggerConfigModel.model_validate(config_obj)

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
        env_metrics = {}

        for inner_metric_logger in self.inner_metrics_loggers:
            inner_metric_logger.collect_env_metrics(data)

            if hasattr(inner_metric_logger, "env_metrics"):
                env_metrics = env_metrics | inner_metric_logger.env_metrics

        self.env_metrics = env_metrics

    def collect_agent_metrics(self, data: AgentControllerData):
        agent_metrics = {}

        for inner_metric_logger in self.inner_metrics_loggers:
            inner_metric_logger.collect_agent_metrics(data)

            if hasattr(inner_metric_logger, "agent_metrics"):
                agent_metrics = agent_metrics | inner_metric_logger.agent_metrics

        self.agent_metrics = agent_metrics

    def get_metrics(self) -> Dict[str, Any]:
        return self.env_metrics | self.agent_metrics

    def report_metrics(self):
        print_metrics(self.get_metrics())