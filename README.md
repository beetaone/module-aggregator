# Aggregator

|                |                                       |
| -------------- | ------------------------------------- |
| Name           | Aggregator                           |
| Version        | v1.0.2                                |
| DockerHub | [beetaone/aggregator](https://hub.docker.com/r/beetaone/aggregator) |
| authors        | Jakub Grzelak, Sanyam Arya                    |

- [Aggregator](#aggregator)
  - [Description](#description)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the beetaone Agent on the edge-node](#set-by-the-beetaone-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)

## Description

Aggregator is a processing module responsible for aggregating data passing through beetaone data services.
Aggregator collects data within a time interval specified by a data service developer, and then it applies a chosen aggregation function.
This module is containerized using Docker.

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

The following module configurations can be provided in a data service designer section on beetaone platform:

| Name                 | Environment Variables     | type     | Description                                              |
| -------------------- | ------------------------- | -------- | -------------------------------------------------------- |
| Interval Unit        | INTERVAL_UNIT             | string   | The unit for time interval (ms, s, m, h, d)              |
| Interval Period      | INTERVAL_PERIOD           | integer  | The time interval on which aggregation will be applied   |
| Function             | FUNCTION                  | string   | Aggregation function to apply (mean, max, spread, median, sum, stddv, count, first, min, last) |
| Input Label          | INPUT_LABEL               | string   | The input label on which anomaly is detected             |
| Output Label         | OUTPUT_LABEL              | string   | The output label as which data is dispatched             |


### Set by the beetaone Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by beetaone agent.

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)  |
| EGRESS_URL            | string | HTTP ReST endpoint for the next module         |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |

## Dependencies

```txt
bottle
requests
```

## Input

Input to this module is JSON body single object:

Example:

```json
{
  temperature: 15,
  input_unit: Celsius
}
```

## Output

Output of this module is JSON body array of objects.

Output of this module is JSON body:

```json
{
    "<OUTPUT_LABEL>": <Processed data>,
}
```

* Here `OUTPUT_LABEL` is specified at the module creation and `Processed data` is data processed by Module Main function.

Example:

```json
{
  meanTemp: 54.7,
}
```