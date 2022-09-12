import logging

from gpiozero import InputDevice

from .. import metrics

logger = logging.getLogger("sensors_exporter")

class Metrics:
    sensor = None

    def __init__(self, name, pin):
        """ Initializes the sensor.

        Keyword arguments:
            name - the name of the sensor, connected to GPIO
            pin - the pin number where the sensor is connected
        """

        self.name = name
        self.pin = pin

        logger.debug(f'[GPIO] Initializing sensor {self.name}')
        self.sensor = InputDevice(self.pin)

    def __del__(self):
        """ Closes the communication bus. """

        self.sensor.close()

    def getSensorData(self):
        """ Reads data from the sensor, returns value """

        logger.debug(f'[GPIO] Reading {self.name} sensor data')
        value = self.sensor.value
    
        return value
    
    def getMetrics(self):
        """ Populates the metrics with sensor data. """

        m_value = self.getSensorData()
        logger.debug('[GPIO] Populating metrics')

        metrics.gpio_value.labels(self.name, 'gpio').set(m_value)
    
