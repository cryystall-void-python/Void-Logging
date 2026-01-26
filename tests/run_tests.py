"""Main file for launching tests"""

import unittest

from tests.rewards.apply_operation_test import ApplyOperationWrapperTestCase
from tests.rewards.base_tests import BaseTestsCase
from tests.rewards.custom_name_test import CustomNameWrapperTestCase
from tests.rewards.default_if_none_test import DefaultIfNoneWrapperTestCase
from tests.rewards.fill_metrics_test import FillMetricsWrapperTestCase
from tests.rewards.logged_combined_reward_test import LoggedCombinedRewardTestCase
from tests.rewards.operations import OperationsTestCase
from tests.rewards.reward_fn_test import RewardFnWrapperTestCase
from tests.rewards.zerosum_test import ZeroSumTestCase


def suite():
    """Test suite declaration

    Returns:
        suite (TestSuite): The created suite
    """
    test_suite = unittest.TestSuite()

    test_suite.addTest(BaseTestsCase())
    test_suite.addTest(LoggedCombinedRewardTestCase())
    test_suite.addTest(ZeroSumTestCase())
    test_suite.addTest(ApplyOperationWrapperTestCase())
    test_suite.addTest(CustomNameWrapperTestCase())
    test_suite.addTest(DefaultIfNoneWrapperTestCase())
    test_suite.addTest(FillMetricsWrapperTestCase())
    test_suite.addTest(RewardFnWrapperTestCase())
    test_suite.addTest(OperationsTestCase())

    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
