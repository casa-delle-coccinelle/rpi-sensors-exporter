import logging

from gpiozero import InputDevice

from .. import metrics

logger = logging.getLogger("sensors_exporter")

class GPIOMetrics:
    sensor = None

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

        logger.debug(f'[GPIO] Initializing sensor {self.name}')
        self.sensor = InputDevice(self.pin)

    def getSensorData(self):
        logger.debug(f'[GPIO] Reading {self.name} sensor data')
        value = self.sensor.value
        self.sensor.close()
    
        return value
    
    def getMetrics(self):

        m_value = self.getSensorData()
        logger.debug('[GPIO] Populating metrics')

        return metrics.gpio_value.labels(self.name, 'gpio').set(m_value)
    
