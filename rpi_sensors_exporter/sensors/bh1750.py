import board
import adafruit_bh1750

from .. import metrics


class Metrics:
    sensor = None

    def __init__(self):

        self.i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(self.i2c)

    def getSensorData(self):
        light = self.sensor.lux
    
        return (light)
    
    def getMetrics(self):

        m_light = self.getSensorData()

        return metrics.vis_light.labels("bh1750", "i2c").set(m_light)    
