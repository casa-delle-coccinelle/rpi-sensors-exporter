import logging

import board
import adafruit_sht4x 

from .. import metrics


class Metrics:
    sensor = None

    def __init__(self):
        """ Initializes the sensor. """

        self.logger = logging.getLogger(__name__)
        self.logger.debug('Initializing sensor')

        self.i2c = board.I2C()
        self.sensor = adafruit_sht4x.SHT4x(self.i2c)
        self.sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

    def getSensorData(self):
        """ Reads data from the sensor, returns temp, humidity. """

        self.logger.debug('Reading sensor data')

        temp, humidity = self.sensor.measurements
        
        return (temp, humidity)
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """

        m_temp, m_hum = self.getSensorData()
        self.logger.debug('Populating metrics')

        metrics.temperature.labels("sht40", "i2c").set(m_temp), metrics.humidity.labels("sht40", "i2c").set(m_hum)
