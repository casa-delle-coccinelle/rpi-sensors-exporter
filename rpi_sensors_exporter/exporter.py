import os

from prometheus_client import make_wsgi_app
from flask import Flask
from waitress import serve

from .sensors import bmp180, bme688, gpio, ads, bh1750, si1145
from . import metrics
from . import config_loader

app = Flask("exporter")

port, config = config_loader.load()


@app.route("/metrics")
def getSensors():
    try:
        sensor = bmp180.BMP180Metrics()
        metrics.initializeMetrics("bmp180")
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bmp180", "i2c").set(1)
    except (OSError):
        pass

    try:
        sensor = bme688.BME688Metrics()
        metrics.initializeMetrics("bme688")
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bme688", "i2c").set(1)
    except (RuntimeError, OSError):
        pass

    try:
        for device in config['gpio_devices']:
            metrics.initializeMetrics("gpio", device['type'])
            sensor = gpio.GPIOMetrics(device['name'], device['pin'])
            sensor.getMetrics()
            metrics.sensor_exporter_info.labels(device['name'], 'gpio').set(1)
    except (AttributeError, TypeError):
        pass


    try:
        for device in config['ads_devices']:
            metrics.initializeMetrics("ads", device['type'])
            try:
                sensor = ads.ADSMetrics(device['name'], device['analog_in'], device['max_value'], device['min_value'])
            except (KeyError):
                sensor = ads.ADSMetrics(device['name'], device['analog_in'])

            sensor.getMetrics()
            metrics.sensor_exporter_info.labels(device['name'], 'adc').set(1)
    except (AttributeError, TypeError):
        pass

    try:
        sensor = bh1750.Metrics()
        metrics.initializeMetrics("bh1750")
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("bh1750", "i2c").set(1)
    except(ValueError):
        pass

    try:
        sensor = si1145.Metrics()
        metrics.initializeMetrics("si1145")
        sensor.getMetrics()
        metrics.sensor_exporter_info.labels("si1145", "i2c").set(1)
    except (OSError):
        pass

    return make_wsgi_app()


def main():
    serve(app, host='0.0.0.0', port=(port or 8080))


if __name__ == '__main__':
    main()

