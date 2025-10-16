# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
