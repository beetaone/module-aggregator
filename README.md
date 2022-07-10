# Python Processing Module Boilerplate

|              |                                                                  |
| ------------ | ---------------------------------------------------------------- |
| name         | Python Processing Module Boilerplate                             |
| version      | v2.0.0                                                           |
| GitHub       | [python-processing-module-boilerplate](https://linktodockerhub/) |
| authors      | Jakub Grzelak, Nithin Saai                                       |

***
## Table of Content

- [Python Processing Module Boilerplate](#python-processing-module-boilerplate)
  - [Table of Content](#table-of-content)
  - [Description](#description)
  - [Directory Structure](#directory-structure)
    - [File Tree](#file-tree)
  - [Module Variables](#module-variables)
  - [As a module developer](#as-a-module-developer)
  - [Module Testing](#module-testing)
  - [Dependencies](#dependencies)
***

## Description 

This is a Python Processing Boilerplate module and it serves as a starting point for developers to build process modules for weeve platform and data services.
Navigate to [As a module developer](#as-a-module-developer) to learn how to use this module. You can also explore our weeve documentation on [weeve Modules](https://docs.weeve.engineering/concepts/edge-applications/weeve-modules) and [module tutorials](https://docs.weeve.engineering/guides/how-to-create-a-weeve-module) to learn more details. 

## Directory Structure

Most important resources:

| name              | description                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| src               | All source code related to the module (API and module code).                                           |
| src/main.py       | Entry-point for the module.                                                                            |
| src/api           | Code responsible for setting module's API and communication with weeve ecosystem.                      |
| src/module        | Code related to the module's business logic. This is working directory for module developers.          |
| docker            | All resources related to Docker (Dockerfile, docker-entrypoint.sh, docker-compose.yml).                |
| test              | All resources related to automating testing of the module in development process.                      |
| example.env       | Holds examples of environment variables for running the module.                                        |
| requirements.txt  | A list of module dependencies.                                                                         |
| Module.yaml       | Module's YAML file that is later used by weeve platform Data Service Designer                          |

### File Tree

```bash
├── src
│   ├── api
│   │   ├── __init__.py
│   │   ├── log.py # log configurations
│   │   ├── processing_thread.py # a separate thread responsible for triggering data processing and sending to the next module
│   │   ├── send_data.py # sends data to the next module
│   │   └── request_handler.py # handles module's API and receives data from a previous module
│   ├── module
│   │   ├── main.py # [*] main logic for the module
│   │   └── validator.py # [*] validation logic for incoming data
│   └── main.py # module entrypoint
├── docker
│   ├── .dockerignore
│   ├── docker-compose.yml
│   ├── docker-entrypoint.sh
│   └── Dockerfile
├── test
│   ├── assets
│   │   ├── input.json # input data for tests (sample module input)
│   │   └── expected_output.json # expected output data for tests (sample module output)
│   ├── boilerplate_test.py # script handling module testing
│   ├── docker-compose.test.yml
│   ├── Dockerfile.listener # dockerfile for a container used to simulate egress endpoint
│   ├── listener.py # script implementing egress endpoint
│   └── test.env # environment variables for tests
├── example.env # sample environment variables for the module
├── Module.yaml # used by weeve platform to generate resource in Data Service Designer section
├── makefile
├── README.md
├── example.README.md # README template for writing module documentation
├── requirements_dev.txt # module dependencies for testing, used for building Docker image
└── requirements.txt # module dependencies, used for building Docker image
```

## Module Variables

There are 5 module variables that are required by each module to correctly function within weeve ecosystem. In development, these variables can overridden for testing purposes. In production, these variables are set by weeve Agent.

| Environment Variables | type   | Description                                       |
| --------------------- | ------ | ------------------------------------------------- |
| MODULE_NAME           | string | Name of the module                                |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)    |
| LOG_LEVEL             | string | Allowed log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Refer to `logging` package documentation. |
| INGRESS_HOST          | string | Host to which data will be received               |
| INGRESS_PORT          | string | Port to which data will be received               |
| EGRESS_URLS           | string | HTTP ReST endpoint for the next module            |

## As a module developer

RECOMMENDED:
Make sure you have [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

Install the dependencies with `make install_dev`

A module developer needs to add all the configuration and business logic.

All the module logic can be written in the module package in `src/module` directory.

   * The files can me modified for the module
      1. `module/validator.py`
         * The function `data_validation` takes the JSON data received from the previous module.
         * Incoming data can be validated here.
         * Checks if data is of type permitted by a module (i.e. `dict` or `list`)>
         * Checks if data contains required fields.
         * Returns Error if data are not valid.
      2. `module/module.py`
         * The function `module_main` takes the JSON data received from the previous module.
         * All the business logic about modules are written here.
         * Returns processed data and error message.

## Module Testing

To test module navigate to `test` directory. In `test/assets` edit both .json file to provide input for the module and expected output. During a test, data received from the listeners are compared against expected output data. You can run tests with `make run_test`.

## Dependencies

The following are module dependencies:

* bottle
* requests

The following are developer dependencies:

* pytest
* flake8
* black
