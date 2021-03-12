# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Removed

## [v0.1.5](https://github.com/isu-avista/portal/releases/tag/v0.1.5) - 2021-03-12
### Added
* Added  `qemu-static-user` package installation to travis.yml to build for arm architecture
* Added a method to `generate_configs.py` that will create the logs directory and log file if they don't exist
* Added pip installation to `install.sh` as it is needed to install docker-compose

### Changed
* Updated `docker_push` script to use buildx to build image for arm architecture

### Removed

## [v0.1.4](https://github.com/isu-avista/portal/releases/tag/v0.1.4) - 2021-02-19
### Added

### Changed
* Updated the system to work with the latest changes to base-server and data modules

### Removed

## [v0.1.3](https://github.com/isu-avista/portal/releases/tag/v0.1.3) - 2021-02-16
### Added

### Changed
* Fixed the travis ci build

### Removed

## [v0.1.2](https://github.com/isu-avista/portal/releases/tag/v0.1.2) - 2021-02-16
### Added
* docker_pus script to automate building docker images and pushing them to dockerhub

### Changed
* Updated the travisci file to fixed automated build and deploy
* Updated the install script to ensure all needed tools exists

### Removed

## [v0.1.1](https://github.com/isu-avista/portal/releases/tag/v0.1.1) - 2021-02-15
### Added
* Added the basic data route to allow for data to enter the portal from the IoT devices
* Added the docker-compose file to run the system
* Added systemd service file
* Added install script

### Changed
* Updated existing tests
* Modified the existing server to correspond to changes in base-server
* Modified the dockerfile to build the docker image
* Updated README to reflect new instructions for installing and running

### Removed

## [v0.1.0](https://github.com/isu-avista/portal/releases/tag/v0.1.0) - 2020-12-15
### Added
* Implemented the basic server component and setup the folder structure to get going
* Setup the requirements
* Implemented the basic components of the client side including authentication (based on
  the IoT service)

### Changed

### Removed
