# WeevAgator

|                |                                       |
| -------------- | ------------------------------------- |
| Name           | WeevAgator                            |
| Version        | v0.0.2                                |
| Dockerhub Link | weevenetwork/weeve-weevagator         |
| authors        | Jakub Grzelak, Sanyam Arya            |

- [WeevAgator](#weevagator)
  - [Description](#description)
  - [Features](#features)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)
  - [Docker Compose Example](#docker-compose-example)

## Description

WeevAgator is a processing module responsible for aggregating data passing through weeve data services.
WeevAgator collects data within a time interval specified by a data service developer, and then it applies a chosen aggregation function.
This module is containerized using Docker.

## Features

- Applies aggregation functions to data
- Flask ReST client
- Request - sends HTTP Request to the next module

Supported functions:
- mean (mean value that arrived within the specified interval)
- max (maximum value)
- spread (maximum - minimum value)
- median (median value recorded within the interval)
- sum (sum of all received values)
- stddv (standard deviation of values)
- count (number of data that arrived within the interval)
- first (first recorded data)
- min (minimum value)
- last (last recorded data)


## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Name                 | Environment Variables     | type     | Description                                              |
| -------------------- | ------------------------- | -------- | -------------------------------------------------------- |
| Interval Unit        | INTERVAL_UNIT             | string   | The unit for time interval (ms, s, m, h, d)              |
| Interval Period      | INTERVAL_PERIOD           | integer  | The time interval on which aggregation will be applied   |
| Function             | FUNCTION                  | string   | Aggregation function to apply (mean, max, spread, median, sum, stddv, count, first, min, last) |
| Input Label          | INPUT_LABEL               | string   | The input label on which anomaly is detected             |
| Data Type            | DATA_TYPE                 | string   | Type of data in the above mentioned label                |
| Output Label         | OUTPUT_LABEL              | string   | The output label as which data is dispatched             |
| Output Unit          | OUTPUT_UNIT               | string   | The output unit in which data is dispatched              |

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

### Set by the weeve Agent on the edge-node

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (INGRESS, PROCESS, EGRESS)  |
| EGRESS_SCHEME         | string | URL Scheme                                     |
| EGRESS_HOST           | string | URL target host                                |
| EGRESS_PORT           | string | URL target port                                |
| EGRESS_PATH           | string | URL target path                                |
| EGRESS_URL            | string | HTTP ReST endpoint for the next module         |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |
| INGRESS_PATH          | string | Path to which data will be received            |

## Dependencies

```txt
Flask==1.1.1
requests
python-decouple
```

## Input

Input to this module is JSON body single object:

Example:

```node
{
  temperature: 15,
  input_unit: Celsius
}
```

## Output

Output of this module is JSON body array of objects.

Output of this module is JSON body:

```node
{
    "<OUTPUT_LABEL>": <Processed data>,
    "output_unit": <OUTPUT_UNIT>,
}
```
 
* Here `OUTPUT_LABEL` and `OUTPUT_UNIT` are specified at the module creation and `Processed data` is data processed by Module Main function.

Example:

```node
{
  meanTemp: 54.7,
  output_unit: Celsius,
}
```

## Docker Compose Example

```yml
version: "3"
services:
  weevagator:
    image: weevenetwork/weeve-weevagator
    environment:
      EGRESS_URL: "https://hookb.in/pzaBWG9rKoSXNNqwBo3o"
      INGRESS_HOST: "0.0.0.0"
      INGRESS_PORT: "5000"
      INTERVAL_UNIT: "ms"
      INTERVAL_PERIOD: 10000
      FUNCTION: "mean"
      INPUT_LABEL: "temperature"
      DATA_TYPE: "float"
      OUTPUT_LABEL: "differentialTemp"
      OUTPUT_UNIT: "Celsius"
    ports:
      - 5000:80
```