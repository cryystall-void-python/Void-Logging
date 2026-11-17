import os
import tempfile
import unittest
from os import PathLike
from typing import Any

from pydantic import BaseModel
from rlgym_learn_algos.logging.metrics_logger import DerivedMetricsLoggerConfig

from rlgym_learn_logging.rlgym_learn.env_metrics_logger import EnvMetricsLogger
from rlgym_learn_logging.rlgym_learn.metric_logger import CustomMetricLogger
from rlgym_learn_logging.rlgym_learn.multi_logger import (
    MultiLogger,
    MultiLoggerConfigModel,
)
from rlgym_learn_logging.rlgym_learn.reward_metrics_logger import RewardMetricsLogger


class RequiresConfig(BaseModel):
    some_config_str: str


class RequiresConfigMetricsLogger(EnvMetricsLogger):
    @property
    def config_model(self) -> type[RequiresConfig]:
        return RequiresConfig

    def load(self, config: DerivedMetricsLoggerConfig):
        self.config = config

    def save_checkpoint(self, folder_path: str | PathLike[str]):
        self.saved_to = folder_path

    def collect_env_metrics(self, data: list[dict[str, Any] | None]):
        self.metrics = {"data": 1}

    def get_metrics(self) -> dict[str, Any]:
        return self.metrics


class MultiLoggerTestCase(unittest.TestCase):
    def runTest(self):
        self.test_init()
        self.test_load()
        self.test_config_count_mismatch()
        self.test_collect_and_checkpoint()

    def test_init(self):
        _multi_logger = MultiLogger(RewardMetricsLogger(), CustomMetricLogger())
        self.assertEqual(len(_multi_logger.inner_metrics_loggers), 2)

    def _load(self, logger: RequiresConfigMetricsLogger) -> MultiLogger:
        _multi_logger = MultiLogger(logger, CustomMetricLogger())
        # As WandbMetricsLogger does with its inner logger's config
        _config = _multi_logger.config_model.model_validate(
            {"inner_metrics_logger_config": [{"some_config_str": "test"}, None]},
            context=_multi_logger,
        )
        _multi_logger.load(
            DerivedMetricsLoggerConfig(
                agent_controller_name="test",
                derived_agent_controller_config=None,
                metrics_logger_config=_config,
                checkpoint_load_folder=None,
            )
        )
        return _multi_logger

    def test_load(self):
        _logger = RequiresConfigMetricsLogger()
        self._load(_logger)
        self.assertIsInstance(_logger.config.metrics_logger_config, RequiresConfig)
        self.assertEqual(_logger.config.metrics_logger_config.some_config_str, "test")

    def test_config_count_mismatch(self):
        _multi_logger = MultiLogger(RewardMetricsLogger(), CustomMetricLogger())
        with self.assertRaises(ValueError):
            MultiLoggerConfigModel.model_validate(
                {"inner_metrics_logger_config": [None]}, context=_multi_logger
            )

    def test_collect_and_checkpoint(self):
        _logger = RequiresConfigMetricsLogger()
        _multi_logger = self._load(_logger)
        # None entries: envs that sent no shared info
        _multi_logger.collect_env_metrics([None])
        self.assertEqual(_multi_logger.get_metrics()["data"], 1)
        with tempfile.TemporaryDirectory() as folder:
            _multi_logger.save_checkpoint(folder)
            self.assertTrue(_logger.saved_to.startswith(folder))
            self.assertTrue(os.path.isdir(_logger.saved_to))
