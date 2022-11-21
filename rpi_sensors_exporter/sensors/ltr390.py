import logging

import board
import adafruit_ltr390

from .. import metrics


class Metrics:
    sensor = None

    def __init__(self):
        """ Initializes the sensor. """

        self.logger = logging.getLogger(__name__)
        self.logger.debug('Initializing sensor')

        self.i2c = board.I2C()
        self.sensor = adafruit_ltr390.LTR390(self.i2c)

    def getSensorData(self):
        """ Reads data from the sensor, returns light, uvIndex """

        self.logger.debug('Reading sensor data')
        light = self.sensor.lux
        uvIndex = self.sensor.uvi
        
        return (light, uvIndex)
    
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """
    
        m_light, m_uvIndex = self.getSensorData()
        self.logger.debug('Populating metrics')

        metrics.amb_light.labels("ltr390", "i2c").set(m_light), metrics.uv_index.labels("ltr390", "i2c").set(m_uvIndex)
