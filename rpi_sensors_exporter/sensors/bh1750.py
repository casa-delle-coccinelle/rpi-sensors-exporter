import logging

import board
import adafruit_bh1750

from .. import metrics

logger = logging.getLogger("sensors_exporter")

class Metrics:
    sensor = None

    def __init__(self):

        logger.debug('[BH1750] Initializing sensor')

        self.i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(self.i2c)

    def getSensorData(self):

        logger.debug('[BH1750] Reading sensor data')
        light = self.sensor.lux
    
        return (light)
    
    def getMetrics(self):

        m_light = self.getSensorData()
        logger.debug('[BH1750] Populating metrics')

        return metrics.vis_light.labels("bh1750", "i2c").set(m_light)    
