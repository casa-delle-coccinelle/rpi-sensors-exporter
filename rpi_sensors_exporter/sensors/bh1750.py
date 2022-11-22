import logging

import board
import adafruit_bh1750

from .. import metrics


class Metrics:
    sensor = None

    def __init__(self):
        """ Initializes the sensor. """

        self.logger = logging.getLogger(__name__)
        self.logger.debug('Initializing sensor')

        self.i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(self.i2c)

    def getSensorData(self):
        """ Reads data from the sensor, returns light. """

        self.logger.debug('Reading sensor data')
        light = self.sensor.lux
    
        return (light)
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """

        m_light = self.getSensorData()
        self.logger.debug('Populating metrics')

        metrics.amb_light.labels("bh1750", "i2c").set(m_light)    
