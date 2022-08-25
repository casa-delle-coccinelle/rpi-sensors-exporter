import logging

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from .. import metrics

logger = logging.getLogger("sensors_exporter")

class ADSMetrics:
    sensor = None

    def __init__(self, name, analog_in, max_value=None, min_value=None):
        self.name = name
        self.analog_in = analog_in
        self.max_value = max_value
        self.min_value = min_value

        logger.debug(f'[ADS] Initializing sensor {self.name}')

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.sensor = AnalogIn(self.ads, self.analog_in)

    def getSensorData(self):

        logger.debug(f'[ADS] Reading {self.name} sensor data')
        voltage = self.sensor.voltage
        value = self.sensor.value
    
        return (voltage, value)
    
    
    def calculatePercentage(self, value):
    
        percent = round((self.max_value - value)*100/(self.max_value - self.min_value), 2)
        return percent
    
    
    def getMetrics(self):

        m_voltage, m_value = self.getSensorData()

        if self.max_value and self.min_value:
            logger.debug(f'[ADS] Calculating percentage metric for sensor {self.name}')
            m_percentage = self.calculatePercentage(m_value)
            logger.debug('[ADS] Populating metrics')
            return metrics.voltage.labels(self.name, 'adc').set(m_voltage), metrics.ads_value.labels(self.name, 'adc').set(m_value), metrics.percentage.labels(self.name, 'adc').set(m_percentage)
        else:
            logger.debug('[ADS] Populating metrics')
            return metrics.voltage.labels(self.name, 'adc').set(m_voltage), metrics.ads_value.labels(self.name, 'adc').set(m_value)
    
