## Development notes
Adding support for new sensor:
* In metrics.py add the necessary metrics depending on the data provided by the sensor, considering metric and label naming best practices - https://prometheus.io/docs/practices/naming/
* Add "Metrics" class in sensors dir, which gets the sensor data and populates the metrics
* Add the corresponding sensor in exporter.py
