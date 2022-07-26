import logging

import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from .. import metrics


class Metrics:
    sensor = None

    def __init__(self, name, analog_in, max_value=None, min_value=None):
        """ Initializes the sensor.

        Keyword arguments:
            name - the name of the sensor, connected to ADS1115
            analog_in - the number of anlogue input pin, where the sensor is connected to ADS1115
            max_value - (optional) the maximum number expected on the pin. Will be used for percentage calculation.
            min_value - (optional) the minimum number expected on the pin. Will be used for percentage calculation.
        """

        self.name = name
        self.analog_in = analog_in
        self.max_value = max_value
        self.min_value = min_value

        self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Initializing sensor {self.name}')

        self.i2c = board.I2C()
        self.ads = ADS.ADS1115(self.i2c)
        self.sensor = AnalogIn(self.ads, self.analog_in)

    def getSensorData(self):
        """ Reads data from the sensor, returns voltage and value """

        self.logger.debug(f'Reading {self.name} sensor data')
        voltage = self.sensor.voltage
        value = self.sensor.value
    
        return (voltage, value)
    
    
    def calculatePercentage(self, value):
        """ Calculates percentage, returns percent. """
    
        percent = round((self.max_value - value)*100/(self.max_value - self.min_value), 2)
        return percent
    
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """

        m_voltage, m_value = self.getSensorData()

        if self.max_value and self.min_value:
            self.logger.debug(f'Calculating percentage metric for sensor {self.name}')
            m_percentage = self.calculatePercentage(m_value)

            self.logger.debug('Populating metrics')
            metrics.voltage.labels(self.name, 'adc').set(m_voltage), metrics.ads_value.labels(self.name, 'adc').set(m_value), metrics.percentage.labels(self.name, 'adc').set(m_percentage)
        else:
            self.logger.debug('Populating metrics')
            metrics.voltage.labels(self.name, 'adc').set(m_voltage), metrics.ads_value.labels(self.name, 'adc').set(m_value)
    
