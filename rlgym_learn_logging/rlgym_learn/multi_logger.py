"""Module for the multi logger"""

import os
from os import PathLike
from typing import Any, Dict, List

from pydantic import BaseModel, Field, ValidationInfo, model_validator
from rlgym_learn_algos.logging import DerivedMetricsLoggerConfig, DictMetricsLogger

INNER_LOGGER_FOLDER = "inner_metrics_logger_{}"


class MultiLoggerConfigModel(BaseModel, extra="forbid"):
    """Config of a MultiLogger: one entry per inner logger, in the same order.
    Use None for loggers without a config (their config_model is None)."""

    inner_metrics_logger_config: List[Any] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def validate_inner_configs(cls, data: Any, info: ValidationInfo) -> Any:
        """When validated with the MultiLogger as context (as WandbMetricsLogger
        does with its inner logger), validates each inner config with its
        logger's config model."""
        multi_logger = info.context
        if not isinstance(multi_logger, MultiLogger) or not isinstance(data, dict):
            return data
        raw_configs = data.get("inner_metrics_logger_config")
        if raw_configs is None:
            raw_configs = [None] * len(multi_logger.inner_metrics_loggers)
        if len(raw_configs) != len(multi_logger.inner_metrics_loggers):
            raise ValueError(
                f"You gave {len(raw_configs)} config objects for "
                f"{len(multi_logger.inner_metrics_loggers)} loggers. Please provide one "
                "per logger (None for a logger without config)."
            )
        configs = []
        for logger, raw in zip(multi_logger.inner_metrics_loggers, raw_configs):
            model = logger.config_model
            if model is None or not isinstance(raw, dict):
                configs.append(None if model is None else raw)
            else:
                configs.append(model.model_validate(raw, context=logger))
        return {**data, "inner_metrics_logger_config": configs}


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
