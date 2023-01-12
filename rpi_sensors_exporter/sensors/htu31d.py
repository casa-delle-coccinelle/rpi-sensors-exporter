import logging

import board
import adafruit_htu31d

from .. import metrics


class Metrics:
    sensor = None

    def __init__(self):
        """ Initializes the sensor. """

        self.logger = logging.getLogger(__name__)
        self.logger.debug('Initializing sensor')

        self.i2c = board.I2C()

        try:
            self.logger.debug('Try default sensor address 0x40')
            self.sensor = adafruit_htu31d.HTU31D(self.i2c)
            self.logger.debug('Sensor uses address 0x40')
        except (OSError, ValueError):
            self.logger.debug('Sensor is not connected on 0x40, trying alternative address')
            self.logger.debug('Try sensor address 0x41')
            self.sensor = adafruit_htu31d.HTU31D(self.i2c, address=0x41)
            self.logger.debug('Sensor uses address 0x41')

    def getSensorData(self):
        """ Reads data from the sensor, returns temp, humidity. """

        self.logger.debug('Reading sensor data')

        temp, humidity = self.sensor.measurements
        
        return (temp, humidity)
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """

        m_temp, m_hum = self.getSensorData()
        self.logger.debug('Populating metrics')

        metrics.temperature.labels("htu31d", "i2c").set(m_temp), metrics.humidity.labels("htu31d", "i2c").set(m_hum)
