import os
import logging
import sys

from prometheus_client import make_wsgi_app
from flask import Flask
from waitress import serve

from .sensors import bmp180, bme688, gpio, ads, bh1750, si1145
from . import metrics
from . import config_loader

app = Flask("exporter")

logger = logging.getLogger("sensors_exporter")


@app.route("/metrics")
def getSensors():
    try:
        logger.debug('----------------BMP180-----------')
        logger.debug('Try read sensor data from BMP180')
        sensor = bmp180.BMP180Metrics()
        logger.info('Sensor type BMP180 is connected to the system')
        logger.debug('Initializing metrics for BMP180 sensor')
        metrics.initializeMetrics("bmp180")
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bmp180", "i2c").set(1)
        logger.debug('----------------BMP180-----------')
    except (OSError):
        logger.info('Sensor type BMP180 is not connected to the system')
        logger.debug('----------------BMP180-----------')
        pass

    try:
        logger.debug('----------------BME688-----------')
        logger.debug('Try read sensor data from BME688')
        sensor = bme688.BME688Metrics()
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
        pass

    try:
        logger.debug('----------------GPIO-----------')
        for device in config['gpio_devices']:
            logger.debug(f"Try read sensor data from GPIO sensor {device['name']}")
            sensor = gpio.GPIOMetrics(device['name'], device['pin'])
            logger.info(f"GPIO sensor {device['name']} is connected to the system")
            logger.debug(f"Initializing metrics for GPIO sensor {device['name']}")
            metrics.initializeMetrics("gpio", device['type'])
            logger.debug('Getting sensor data')
            sensor.getMetrics()
            metrics.sensor_exporter_info.labels(device['name'], 'gpio').set(1)
        logger.debug('----------------GPIO-----------')
    except (AttributeError, TypeError):
        logger.info('There are no GPIO sensors connected to the system')
        logger.debug('----------------GPIO-----------')
        pass


    try:
        logger.debug('----------------ADS-----------')
        for device in config['ads_devices']:
            logger.debug(f"Try read sensor data from ADS sensor {device['name']}")
            try:
                sensor = ads.ADSMetrics(device['name'], device['analog_in'], device['max_value'], device['min_value'])
                logger.debug(f"Min and max values are configured for sensor {device['name']}, percentage will be calculated")
                logger.info(f"ADS sensor {device['name']} is connected to the system")
            except (KeyError):
                sensor = ads.ADSMetrics(device['name'], device['analog_in'])
                logger.debug(f"Min and max values are NOT configured for sensor {device['name']}, percentage will NOT be calculated")
                logger.info(f"ADS sensor {device['name']} is connected to the system")

            logger.debug(f"Initializing metrics for ADS sensor {device['name']}")
            metrics.initializeMetrics("ads", device['type'])
            logger.debug('Getting sensor data')
            sensor.getMetrics()
            metrics.sensor_exporter_info.labels(device['name'], 'adc').set(1)
            logger.debug('----------------ADS-----------')
    except (AttributeError, TypeError):
        logger.info('There are no ADS sensors connected to the system')
        logger.debug('----------------ADS-----------')
        pass

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
        pass

    try:
        logger.debug('----------------SI1145-----------')
        logger.debug('Try read sensor data from SI1145')
        sensor = si1145.Metrics()
        logger.info('Sensor type SI1145 is connected to the system')
        logger.debug('Initializing metrics for SI1145 sensor')
        metrics.initializeMetrics("si1145")
        logger.debug('Getting sensor data')
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("si1145", "i2c").set(1)
        logger.debug('----------------SI1145-----------')
    except (OSError):
        logger.info('Sensor type SI1145 is not connected to the system')
        logger.debug('----------------SI1145-----------')
        pass

    return make_wsgi_app()


def main():
    global config

    config_loader.logs_setup()
    port, config = config_loader.load()
    serve(app, host='0.0.0.0', port=(port or 8080))


if __name__ == '__main__':
    main()

