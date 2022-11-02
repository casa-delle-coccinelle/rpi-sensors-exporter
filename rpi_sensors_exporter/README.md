## Development notes
Adding support for new sensor:
* In metrics.py add the necessary metrics depending on the data provided by the sensor, considering metric and label naming best practices - https://prometheus.io/docs/practices/naming/
* If the given metric is not already exported, add global variable to hold the metric object.
* Add the sensor name in the list with supported sensors in metric.py docstring.
* Add "Metrics" class in sensors dir, which gets the sensor data and populates the metrics
* Add the corresponding sensor in exporter.py. Keep in mind that depending on the underlying library for the specific sensor it is possible that exception different then expected is thrown if a sensor is not connected.
