import unittest
from typing import Any

from pydantic import BaseModel
from rlgym_learn_algos.logging.dict_metrics_logger import DictMetricsLogger
from rlgym_learn_algos.logging.metrics_logger import DerivedMetricsLoggerConfig

from rlgym_learn_logging.rlgym_learn.metric_logger import CustomMetricLogger
from rlgym_learn_logging.rlgym_learn.multi_logger import (
    MultiLogger,
    MultiLoggerAdditionalDerivedConfig,
    MultiLoggerConfigModel,
)
from rlgym_learn_logging.rlgym_learn.reward_metrics_logger import RewardMetricsLogger


class RequiresConfig(BaseModel):
    some_config_str: str


class RequiresConfigMetricsLogger(DictMetricsLogger[RequiresConfig, None, None]):
    def load(self, config: DerivedMetricsLoggerConfig[RequiresConfig, None]):
        self.config = config

    def collect_agent_metrics(self, data: None):
        assert hasattr(self, "config"), "Need config to run"
        assert hasattr(self, "_validated"), "Need to be validated to run"
        self.metrics = {"data": 1}

    def validate_config(self, config_obj: dict[str, Any]) -> RequiresConfig:
        self._validated = True
        return RequiresConfig.model_validate(config_obj)


class MultiLoggerTestCase(unittest.TestCase):
    def runTest(self):
        self.test_init()
        self.test_load()

    def test_init(self):
        _multi_logger = MultiLogger(RewardMetricsLogger(), CustomMetricLogger())

        self.assertEqual(len(_multi_logger.inner_metrics_loggers), 2)

    def test_load(self):
        _logger = RequiresConfigMetricsLogger()
        _multi_logger = MultiLogger(_logger, CustomMetricLogger())

        _config = MultiLoggerConfigModel(
            inner_metrics_logger_config=[RequiresConfig(some_config_str="test"), None]
        )

        _multi_logger.validate_config(_config.model_dump())

        _multi_logger.load(
            DerivedMetricsLoggerConfig(
                agent_controller_name="test",
                checkpoint_load_folder=None,
                metrics_logger_config=_config,
                additional_derived_config=MultiLoggerAdditionalDerivedConfig(
                    inner_metrics_logger_additional_derived_config=[None, None]
                ),
            )
        )

        self.assertEqual(len(_multi_logger.inner_metrics_loggers), 2)
        self.assertIn("config", dir(_logger))
        self.assertIn("_validated", dir(_logger))
