# rpi-sensors-exporter

Just for fun/learning python project which exports sensor data from various Raspberry Pi sensors as prometheus metrics.

Currently supported sensors are:
* BMP180 Barometric Pressure/Temperature/Altitude Sensor - https://www.adafruit.com/product/1603
* BME688 Temperature, Humidity, Pressure and Gas Sensor - https://www.adafruit.com/product/5046
* BH1750 Ambient Light Sensor - https://learn.adafruit.com/adafruit-bh1750-ambient-light-sensor
* SI1145 Digital UV Index / IR / Visible Light Sensor - https://www.adafruit.com/product/1777
* ADS1115 16-Bit ADC to connect sensors of different types which provide analog data - https://www.adafruit.com/product/1085 (tested with two soil moisture sensors - Capacitive v1.2 (https://www.amazon.com/Gikfun-Capacitive-Corrosion-Resistant-Detection/dp/B07H3P1NRM) and fc-28 (https://www.amazon.in/xcluma-Moisture-Humidity-Arduino-Respberry/dp/B071LH5Z9D ))
* Generic GPIO sensors - scipt will export data (0 or 1) depending on the voltage level on a given GPIO pin.
