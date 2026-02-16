# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

*

### Changed

*

### Fixed

* Scheduler creating new sessions with the remote Omni API on every tick by reusing a single API instance across scheduling tasks

## [0.3.13] - 2026-01-24

### Fixed

* Type preservation in `sum_results` and `empty_results` to ensure integer fields remain integers
* Added comprehensive tests for type preservation in results aggregation functions

## [0.3.12] - 2026-01-24

### Fixed

* Issue with overlapping variable in `sum_result`

## [0.3.11] - 2026-01-24

### Fixed

* Type coercion issue in `sum_results` by using dynamic default values based on inferred types

## [0.3.10] - 2026-01-11

### Added

* Display Slack token and channel on about page for admin users

## [0.3.9] - 2025-07-20

### Changed

* Bumped packages

## [0.3.8] - 2025-07-20

### Changed

* Bumped packages

### Fixed

* Unit tests in CI

## [0.3.7] - 2025-05-25

### Changed

* Base year to 2025

## [0.3.6] - 2024-04-05

### Fixed

* Issue with `__init__.py` import

## [0.3.5] - 2024-04-05

### Fixed

* Issue with document type selection for submission

## [0.3.4] - 2024-04-05

### Changed

* Better criteria in selection of documents, based on `digest_document_type`

## [0.3.3] - 2024-04-05

### Fixed

* Code syntax issue
* Add more black syntax structure

## [0.3.2] - 2024-04-05

### Changed

* Code structure making it `black` compliant

## [0.3.1] - 2022-06-28

### Fixed

* Issue related to metadata import and initials

## [0.3.0] - 2022-06-25

### Added

* Support for the `orderable` field in the metadata CSV

## [0.2.7] - 2022-02-05

### Added

* Long description support to `setup.py`

## [0.2.6] - 2022-02-04

### Changed

* Better pre validation of prices in XLS upload

## [0.2.5] - 2022-02-04

### Changed

* Float based casting in XLS upload

## [0.2.4] - 2022-02-04

### Changed

* Bumped dependencies

## [0.2.3] - 2021-12-30

### Changed

* Changed base year to 2022

## [0.2.2] - 2021-08-28

### Fixed

* Issue with Python 2 where the `enum` package was not being imported

## [0.2.1] - 2021-07-05

### Changed

* Deploy structure moved to GitHub Actions

## [0.2.0] - 2021-07-05

### Added

* Support for the initials as features in metadata
