### Configuration
Supported are command line argument and environment variables for configuration. Command line arguments will take precedence over the environment variables. 
* Command line

        python -m rpi_sensors_exporter [-h] [-p PORT] [-c CONFIG_FILE] [-v] [-d]


| Option |Default| Description |Required|Since version|
|--|--|--|--|--|
| -p, --port |8080| The port number on which the exporter will run |No| 0.0.1 |
| -c, --config_file |N/A| Path to the exporter's configuration file (*please refer to "Configuration file format" section for more information*) |No |0.0.1|
| -v, --verbose |N/A| Enables exporter's INFO logs on stdout |No |0.0.1|
| -d, --debug | N/A | Enables exporter's INFO and DEBUG logs on stdout | No | 0.0.1|
| -h, --help | N/A | Prints all supported arguments|No|0.0.1

* Environment variables

The following environment variables are supported

| Option |Default| Description |Required|Since version|
|--|--|--|--|--|
| SENSORS_EXPORTER_PORT |8080| The port number on which the exporter will run |No| 0.0.1 |
| SENSORS_EXPORTER_CONFIG |N/A| Path to the exporter's configuration file (*please refer to "Configuration file format" section bellow for more information*) |No |0.0.1|


### Configuration file format
YAML formatted document with optional configuration for sensors connected to GPIO or ADC:

| Configuration | Description |Type|Required|Since version|
|--|--|--|--|--|
| gpio_devices | A list of dictionaries describing GPIO devices connected to the system |list|No| 0.0.1 |
| gpio_devices.name | Name of the sensor, will be added as sensor=${name} label to the metrics  |str|Yes| 0.0.1 |
| gpio_devices.type | Type of the sensor, will be used as is for metric name. If multiple devices are connected to different GPIO pins, make sure that the type is unique. |str|Yes| 0.0.1 |
| gpio_devices.pin | GPIO pin on which the sensor is connected to the system, should be between 0 and 27 inclusive |int|Yes| 0.0.1 |
| ads_devices | A list of dictionaries describing devices connected to the ADC (Analogue-Digital Converter) |list|No| 0.0.1 |
| ads_devices.name | Name of the sensor, will be added as sensor=${name} label to the metrics |str|Yes| 0.0.1 |
| ads_devices.type | Type of the sensor, will be used in metrics name construction - ${type}_value, ${type}_voltage and ${type}_percentage. If multiple devices are connected to different ADS inputs, make sure that the type is unique. |str|Yes| 0.0.1 |
| ads_devices.analog_in | Analogue input pin number of the ADC, should be between 0 and 3 inclusive |int|Yes| 0.0.1 |
| ads_devices.max_value | The maximum of the values reported by ADC, will be used for percentage calculation of ads_devices.type metric (*see notes bellow*) |int|No| 0.0.1 |
| ads_devices.min_value | The minimum of the values reported by ADC, will be used for percentage calculation of ads_devices.type metric (*see notes bellow*)|int |No| 0.0.1 |

Validation of the configuration file is performed on boot and if it is not valid, an exception will be raised. Example of a valid configuration file for one rain drops sensor, connected on GPIO pin 26 and two different soil moisture sensors, connected to ADC is:

    gpio_devices:
      - name: "mh-rd"
        type: "rain_drops"
        pin: 26
    ads_devices:
      - name: "capacitive-v1.2"
        type: "soil_moisture"
        analog_in: 0
        max_value: 32767
        min_value: 23656
      - name: "fc-28"
        type: "soil_moisture"
        analog_in: 1
        max_value: 32767
        min_value: 16726


*Some notes on **ads_devices.max_value** and **ads_devices.min_value**:*

Analogue data provided by some sensors is under the form of output voltage deviation, which ADC represents as numbers. Bigger ADC resolutions provide larger numbers which results in more accurate calculations. For example 16-bit ADC provides 16-bit integer representation of the input voltage from the sensor connected to it. Numerous factors affect the output voltage of the sensor, e.g. power supply voltage (usually can vary between 3.3V and 5V), electrical conductivity of the environment (sand, soil, air, etc.) where the sensor is located and more. For each sensor connected to ADC, the exporter provides metrics ${ads_devices_type}_voltage as well as ${ads_devices_type}_value from which max_value and min_value can be retrieved and configured for each sensor. max_value represents 0% moisture and min_value represent 100% moisture.

For example, the following approach was used to calibrate the capacitive soil moisture sensor. Although it is not 100% accurate, it is a good starting point:
* Place the sensor in glass of water. The output voltage of the sensor decreases as well the raw value. This gives you the min_value configuration (100% moisture). With 5V power supply and 16-bit ADC and measurements for 30 minutes this gave me 23656.
* Get the sensor out of the water and leave it to dry out. The output voltage of the sensor increases (it will be close to the power supply voltage) as well the raw value. This gives you the max_value configuration (0% moisture). With 5V power supply and 16-bit ADC this number should be something like 32767.
* Place the sensor in the soil you want to collect measurements for and configure the calibration values in the exporter. The exporter will now export ${ads_devices_type}_percentage metric in addition to voltage and value metrics. Keep in mind that soil type, soil compaction and fertilizers will affect the sensor's measurements, so a couple of iterations may be necessary to adjust the calibration based on real life data.
