"""Module for the base class of the shared-info-based metrics loggers"""

from abc import ABC
from os import PathLike
from typing import Any

from rlgym_learn_algos.logging import DerivedMetricsLoggerConfig, DictMetricsLogger


class EnvMetricsLogger(
    DictMetricsLogger[Any, None, Any, Any, Any, Any, Any, Any, Any, Any], ABC
):
    """Base for loggers that only read the env processes' shared info
    (collect_env_metrics): no config, no agent controller data, nothing to
    checkpoint. Subclasses implement collect_env_metrics and get_metrics."""

    @property
    def config_model(self) -> None:
        return None

    def collect_agent_metrics(self, data: Any) -> None:
        pass

    def load(self, config: DerivedMetricsLoggerConfig) -> None:
        pass

    def save_checkpoint(self, folder_path: str | PathLike[str]) -> None:
        pass
