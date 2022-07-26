import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import metrics


class ADSMetrics:
    sensor = None

    def __init__(self, name, analog_in, max_value=None, min_value=None):
        self.name = name
        self.analog_in = analog_in
        self.max_value = max_value
        self.min_value = min_value

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.sensor = AnalogIn(self.ads, self.analog_in)

    def getSensorData(self):
        voltage = self.sensor.voltage
        value = self.sensor.value
    
        return (voltage, value)
    
    
    def calculatePercentage(self, value):
    
        percent = round((self.max_value - value)*100/(self.max_value - self.min_value), 2)
        return percent
    
    
    def getMetrics(self):

        m_voltage, m_value = self.getSensorData()

        if self.max_value and self.min_value:
            m_percentage = self.calculatePercentage(m_value)
            return metrics.voltage.labels(self.name, 'adc').set(m_voltage), metrics.ads_value.labels(self.name, 'adc').set(m_value), metrics.percentage.labels(self.name, 'adc').set(m_percentage)
        else:
            return metrics.voltage.labels(self.name, 'adc').set(m_voltage), metrics.ads_value.labels(self.name, 'adc').set(m_value)
    
