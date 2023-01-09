import os
import logging
import sys

from prometheus_client import make_wsgi_app
from flask import Flask
from waitress import serve

from .sensors import bmp180, bme688, gpio, ads1115, bh1750, ltr390, sht40, sht31d
from . import metrics
from . import config_loader

app = Flask("sensors_exporter")

logger = logging.getLogger(__name__)


@app.route("/metrics")
def getSensors():
    """ Tries to read data from each sensor. It is expected that not all sensors are connected to the system. """
    try:
        logger.debug('----------------BMP180-----------')
        logger.debug('Try read sensor data from BMP180')
        sensor = bmp180.Metrics()
        logger.info('Sensor type BMP180 is connected to the system')
        logger.debug('Initializing metrics for BMP180 sensor')
        metrics.initializeMetrics("bmp180")
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bmp180", "i2c").set(1)
        logger.debug('----------------BMP180-----------')
    except (OSError):
        logger.info('Sensor type BMP180 is not connected to the system')
        logger.debug('----------------BMP180-----------')

    try:
        logger.debug('----------------BME688-----------')
        logger.debug('Try read sensor data from BME688')
        sensor = bme688.Metrics()
        logger.info('Sensor type BME688 is connected to the system')
        logger.debug('Initializing metrics for BME688 sensor')
        metrics.initializeMetrics("bme688")
        logger.debug('Getting sensor data')
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bme688", "i2c").set(1)
        logger.debug('----------------BME688-----------')
    except (RuntimeError):
        logger.info('Sensor type BME688 is not connected to the system')
        logger.debug('----------------BME688-----------')
    try:
        logger.debug('----------------SHT40-----------')
        logger.debug('Try read sensor data from SHT40')
        sensor = sht40.Metrics()
        logger.info('Sensor type SHT40 is connected to the system')
        logger.debug('Initializing metrics for SHT40 sensor')
        metrics.initializeMetrics("sht40")
        logger.debug('Getting sensor data')
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("sht40", "i2c").set(1)
        logger.debug('----------------SHT40-----------')
    except (ValueError):
        logger.info('Sensor type SHT40 is not connected to the system')
        logger.debug('----------------SHT40-----------')
    try:
        logger.debug('----------------SHT31D-----------')
        logger.debug('Try read sensor data from SHT31D')
        sensor = sht31d.Metrics()
        logger.info('Sensor type SHT31D is connected to the system')
        logger.debug('Initializing metrics for SHT31D sensor')
        metrics.initializeMetrics("sht31d")
        logger.debug('Getting sensor data')
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("sht31d", "i2c").set(1)
        logger.debug('----------------SHT31D-----------')
    except (ValueError):
        logger.info('Sensor type SHT31D is not connected to the system')
        logger.debug('----------------SHT31D-----------')
    try:
        logger.debug('----------------GPIO-----------')
        for device in config['gpio_devices']:
            logger.debug(f"Try read sensor data from GPIO sensor {device['name']}")
            sensor = gpio.Metrics(device['name'], device['pin'])
            logger.info(f"GPIO sensor {device['name']} is connected to the system")
            logger.debug(f"Initializing metrics for GPIO sensor {device['name']}")
            metrics.initializeMetrics("gpio", device['type'])
            logger.debug('Getting sensor data')
            sensor.getMetrics()
            metrics.sensor_exporter_info.labels(device['name'], 'gpio').set(1)
        logger.debug('----------------GPIO-----------')
    except (KeyError, AttributeError, TypeError):
        logger.info('There are no GPIO sensors connected to the system')
        logger.debug('----------------GPIO-----------')


    try:
        logger.debug('----------------ADS1115-----------')
        for device in config['ads_devices']:
            logger.debug(f"Try read sensor data from ADS1115 sensor {device['name']}")
            try:
                sensor = ads1115.Metrics(device['name'], device['analog_in'], device['max_value'], device['min_value'])
                logger.debug(f"Min and max values are configured for sensor {device['name']}, percentage will be calculated")
                logger.info(f"ADS1115 sensor {device['name']} is connected to the system")
            except (KeyError):
                sensor = ads1115.ADSMetrics(device['name'], device['analog_in'])
                logger.debug(f"Min and max values are NOT configured for sensor {device['name']}, percentage will NOT be calculated")
                logger.info(f"ADS1115 sensor {device['name']} is connected to the system")

            logger.debug(f"Initializing metrics for ADS1115 sensor {device['name']}")
            metrics.initializeMetrics("ads1115", device['type'])
            logger.debug('Getting sensor data')
            sensor.getMetrics()
            metrics.sensor_exporter_info.labels(device['name'], 'adc').set(1)
            logger.debug('----------------ADS1115-----------')
    except (KeyError, AttributeError, TypeError):
        logger.info('There are no ADS sensors connected to the system')
        logger.debug('----------------ADS1115-----------')

    try:
        logger.debug('----------------BH1750-----------')
        logger.debug('Try read sensor data from BH1750')
        sensor = bh1750.Metrics()
        logger.info('Sensor type BH1750 is connected to the system')
        logger.debug('Initializing metrics for BH1750 sensor')
        metrics.initializeMetrics("bh1750")
        logger.debug('Getting sensor data')
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bh1750", "i2c").set(1)
        logger.debug('----------------BH1750-----------')
    except(ValueError):
        logger.info('Sensor type BH1750 is not connected to the system')
        logger.debug('----------------BH1750-----------')

    try:
        logger.debug('----------------LTR390-----------')
        logger.debug('Try read sensor data from LTR390')
        sensor = ltr390.Metrics()
        logger.info('Sensor type LTR390 is connected to the system')
        logger.debug('Initializing metrics for LTR390 sensor')
        metrics.initializeMetrics("ltr390")
        logger.debug('Getting sensor data')
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("ltr390", "i2c").set(1)
        logger.debug('----------------LTR390-----------')
    except (ValueError):
        logger.info('Sensor type LTR390 is not connected to the system')
        logger.debug('----------------LTR390-----------')

    return make_wsgi_app()


def main():
    """ Loads and sets configurations, starts the server """
    global config

    config_loader.logs_setup()
    port, config = config_loader.load()

    metrics.initializeMetrics()

    serve(app, host='0.0.0.0', port=(port or 8080))


if __name__ == '__main__':
    main()

