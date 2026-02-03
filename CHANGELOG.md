# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Some logs had a lot of spaces

## [0.3.1] - 26-01-2026

### Changed

- The `Logged` class is not a Generic anymore and can't be templated anymore
- The `DefaultIfNoneWrapper` constructor now accepts any type instead of just float, still defaults to 0

### Fixed

- `PlayerBallHitForceMetricSharedInfoProvider` now doesn't throw warnings for invalid values
- The division of the `Logged` class was broken (essentially adding instead of substracting), this is now fixed
- The `FillMetricsWrapper` was also rewriting existing metrics, which was not intended

## [0.3.0]

### Added

- You can now specify in advance the metrics of the reward in the `metrics` property
- `PlayerOnGroundRatioMetricSharedInfoProvider` to get the ratio of the agent being on ground
- `GoalScoreSpeedSharedInfoProvider` to get the average goal score speed
- `PlayerBallHitHeightMetricSharedInfoProvider` to get the average ball hit height
- Added a bunch of wrappers that can be chained instead of the `LoggedCombinedRewardArg`
  - `RewardFnWrapper` to manually transform a "normal" reward function into a logged one
  - `DefaultIfNoneWrapper` to return a certain value in case the reward function returns None (doesn't trigger any metric), returns 0 by default
  - `WeightedWrapper` to weight the result of a reward
  - `ZeroSumWrapper` to transform a logged reward into a zero summed logged reward
  - `ConditionWrapper` to trigger a reward only if the agent respects a given condition
  - `CustomNameWrapper` to give a custom name to the reward
  - `ChainWrapper` to be able to use chain function such as `.zero_sum()`, `.weight()`, etc. Making multi-wrappers operations easier
  - `FillMetricsWrapper` to fill each metric (within the `metrics` property) value with 0 to mimic an empty pass
  - `DebugWrapper` to print the metric in a tree-shape output
  - `TestWrapper` to check whether the reward is "valid" (correct amount of outputs, sum check)
  - `ApplyOperationWrapper` to apply an operation after computing the reward

### Fixed

- Add `PlayerOnGroundRatioMetricSharedInfoProvider` to the API
- Allow logged rewards to only have one player triggering a log

### Changed

- Renamed `RewardLogger` to `RewardMetricsLogger`
- Reworked the Logged reward to not need to compute and prepare the logging, this allows more control for wrappers
- Moved `LoggedWrapper` to the API instead of internal use to allow users to use it
- Renamed `LoggedWrapper` to `RewardFnWrapper` to reflect its actual job

### Removed

- Removed `LoggedCombinedRewardArg`

## [0.2.3]

### Added

- `MultiLogger` -> Allows you to have multiple metric loggers inside one logger + prettier print for all metrics

### Fixed

- If the metric logger can't find any player / state related metrics, it will not die but rather log nothing
- `LoggedCombinedReward` was not accounting for the weight in the agent's reward (but was accounting it for the logs), leading to reward logs being wrong

## [0.2.2] - 2025-09-28

### Changed

- `MetricSharedInfoProvider` is now a generic! It means you can use it for stuff other than Rocket League
- `PlayerMetricSharedInfoProvider` and `StateMetricSharedInfoProvider` have been moved to the `rocket_league` subpackage as concrete rocket league implementations of the metric provider
- The ball and player loggers have been moved in according subpackages to control the imports better
- `CustomMetricLogger` now supports optional data, it means you are not forced to return a value and can very well return None, it'll then be ignored

## [0.2.1] - 2025-09-24

### Fixed

- Repaired the metric logging not working as intended
- Various API fixes
- Fixed `BallAccelerationMetricSharedInfoProvider` having the wrong condition for deceleration

## [0.2.0] - 2025-09-24

### Changed

- The API has been changed to be more user-friendly and only giving the actual imports rather than internal elements

### Added

- `MetricSharedInfoProvider` -> Allows you to calculate and place a metric of your choice in the shared info
- `PlayerMetricSharedInfoProvider` -> Allows you to calculate and place a player metric of your choice in the shared info
- `StateMetricSharedInfoProvider` -> Allows you to calculate and place a state metric of your choice in the shared info
- `CustomMetricLogger` -> The rlgym-learn's metric logger to withdraw the state/players metrics from the shared info
- Added a bunch of implementations for various metrics by default

## [0.1.0] - 2025-09-24

### Added

- `LoggedReward` -> Allows you to log any metric contributing to the reward
- `LoggedCombinedReward` -> Allows you to log multiple rewards (be it non loggable or not!)
- `RewardLogger` -> The rlgym-learn's metric logger to withdraw the reward metrics from the shared info
- `RewardSharedInfoProvider` -> The rlgym's shared info provider to prepare the reward metrics
