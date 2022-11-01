# rpi-sensors-exporter

### Project overview
Just for fun/learning python project which exports sensor data from various Raspberry Pi sensors as Prometheus metrics.

Currently supported sensors are:
* BMP180 Barometric Pressure/Temperature/Altitude Sensor - https://www.adafruit.com/product/1603
* BME688 Temperature, Humidity, Pressure and Gas Sensor - https://www.adafruit.com/product/5046
* BH1750 Ambient Light Sensor - https://learn.adafruit.com/adafruit-bh1750-ambient-light-sensor
* LTR390 UV Sensor - https://learn.adafruit.com/adafruit-ltr390-uv-sensor/overview-2
* ADS1115 16-Bit ADC to connect sensors of different types which provide analog data - https://www.adafruit.com/product/1085 (tested with two soil moisture sensors - Capacitive v1.2 (https://www.amazon.com/Gikfun-Capacitive-Corrosion-Resistant-Detection/dp/B07H3P1NRM) and fc-28 (https://www.amazon.in/xcluma-Moisture-Humidity-Arduino-Respberry/dp/B071LH5Z9D ))
* Generic GPIO sensors - script will export data (0 or 1) depending on the voltage level on a given GPIO pin.

The intention is collected data to be used in various garden automations such as watering (watering only when needed, disabling the system when there is chance of freezing, etc.), shade and rain covers to protect the plants and provide optimal growing conditions and more. Constant monitoring of the weather conditions gives a good orientation when to do gerdening specific tasks, e.g. when to plant or sow, when to spray, etc.

### Usage
rpi_sensors_exporter package can be installed using pip:

    sudo pip install git+https://github.com/casa-delle-coccinelle/rpi-sensors-exporter@v0.0.1

Or with ansible role, available in https://github.com/casa-delle-coccinelle/ansible-role-rpi-sensors-exporter
Start from the command line:

    python -m rpi_sensors_exporter [-h] [-p PORT] [-c CONFIG_FILE] [-v] [-d]

For more information on how to configure and use the package, please visit [docs](./docs) directory of the project.

### Examples
As the setup is hard to reproduce, detailed description of the setup used during dev/test can be found in [examples](./examples) directory of the project, including:
* schematics and photos of the setup
* sample dashboard for Grafana
* screenshots of the dashboard with real data 
* sample k8s manifests for Prometheus k8s operator configuration
* sample logs of the package

