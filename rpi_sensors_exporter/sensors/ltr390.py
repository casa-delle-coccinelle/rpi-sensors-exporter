import logging

import board
import adafruit_ltr390

from .. import metrics

logger = logging.getLogger("sensors_exporter")

class Metrics:
    sensor = None

    def __init__(self):
        """ Initializes the sensor. """

        logger.debug('[LTR390] Initializing sensor')

        self.i2c = board.I2C()
        self.sensor = adafruit_ltr390.LTR390(self.i2c)

    def getSensorData(self):
        """ Reads data from the sensor, returns light, uvIndex """

        logger.debug('[LTR390] Reading sensor data')
        light = self.sensor.lux
        uvIndex = self.sensor.uvi
        
        return (light, uvIndex)
    
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """
    
        m_light, m_uvIndex = self.getSensorData()
        logger.debug('[LTR390] Populating metrics')

        metrics.amb_light.labels("ltr390", "i2c").set(m_light), metrics.uv_index.labels("ltr390", "i2c").set(m_uvIndex)
