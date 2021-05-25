# WeevAgator

| | |
| --- | ---|
| version | `v0.0.1` |
| authors | `Jakub Grzelak`, `Sanyam Arya` |
| docker image | `weevenetwork/weeve-weevagator` |
| tech tags | `Python`, `Flask`, `Numpy`, `Docker` |

_WeevAgator is a processing module responsible for aggregating data passing through weeve data services._ 
_WeevAgator collects data within a time interval specified by a data service developer, and then it applies a chosen aggregation function._
_This module is containerized using Docker._

The following module features must be provided by a developer in a data service designer section on weeve platform:
* **Interval Unit** - the unit for time interval,
  * ms    _(milliseconds)_
  * s     _(seconds)_
  * m     _(minutes)_
  * h     _(hours)_
  * d     _(days)_
* **Interval Period** - the time interval on which aggregation will be applied,
  * type: integer
* **Function** - the aggregation function to apply,
  * mean      _(mean value that arrived within the specified interval)_
  * max       _(maximum value)_
  * spread    _(maximum - minimum value)_
  * median    _(median value recorded within the interval)_
  * sum       _(sum of all received values)_
  * stddv     _(standard deviation of values)_
  * count     _(number of data that arrived within the interval)_
  * first     _(first recorded data)_
  * min       _(minimum value)_
  * last      _(last recorded data)_
* **Input Label** - the input label on which anomaly is detected,
  * type: string
* **Data Type** - type of data in the above mentioned label,
  * float
  * integer
* **Output Label** - the output label as which data is dispatched,
  * type: string
* **Output Unit** - the output unit in which data is dispatched,
  * type: string

Other features required for establishing the inter-container communication between modules in a data service are set by weeve server.
These include: egress api host, egress api method, handler host and port.

WeevAgator requires the following Python packages that will be installed on a container built:
* Flask v1.1.1
* requests
* NumPy
* python-decouple v3.4