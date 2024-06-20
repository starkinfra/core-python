# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to the following versioning pattern:

Given a version number MAJOR.MINOR.PATCH, increment:

- MAJOR version when the **API** version is incremented. This may include backwards incompatible changes;
- MINOR version when **breaking changes** are introduced OR **new functionalities** are added in a backwards compatible manner;
- PATCH version when backwards compatible bug **fixes** are implemented.


## [Unreleased]

## [0.5.0] - 2024-06-20
### Changed
- error parse by raw methods
### Fixed
- get public key method 

## [0.4.0] - 2024-06-19
### Changed
- raw methods response type
### Fixed
- prefix param

## [0.3.2] - 2024-05-27
### Fixed
- get_public_key request parameters

## [0.3.1] - 2024-05-23
### Added
- tests to all rest methods
### Fixed
- fetch Response class

## [0.3.0] - 2024-05-21
### Added
- delete_raw to rest utils
- parse function to Rest methods

## [0.2.1] - 2024-03-06
### Fixed
- PUT method reference

## [0.2.0] - 2024-03-05
### Added
- put_raw to rest utils

## [0.1.1] - 2023-05-19
### Fixed
- expand attribute case cast

## [0.1.0] - 2023-04-13
### Added
- post_raw to rest utils

## [0.0.9] - 2022-10-07
### Fixed
- Fixed query() cursor and limit iteration

## [0.0.8] - 2022-09-07
### Fixed
- Non-strict JSON parsing on parse_and_verify

## [0.0.7] - 2022-09-07
### Added
- starksign to hosts
- PublicUser to enable public route access without credentials
- post_sub_resource to rest utils

## [0.0.6] - 2022-07-04
### Added
- verify function outside parse_and_verify

## [0.0.5] - 2022-06-22
### Fixed
- validation for masked dates and datetimes

## [0.0.4] - 2022-06-09
### Fixed
- validation for masked dates and datetimes

## [0.0.3] - 2022-05-11
### Added
- SubResource cast on api.cast_values method

## [0.0.2] - 2022-03-14
### Added
- starkcore API basic functionalities for starkbank and starkinfra 
