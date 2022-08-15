from gpiozero import InputDevice

from .. import metrics


class GPIOMetrics:
    sensor = None

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

        self.sensor = InputDevice(self.pin)

    def getSensorData(self):
        value = self.sensor.value
        self.sensor.close()
    
        return value
    
    def getMetrics(self):

        m_value = self.getSensorData()

        return metrics.gpio_value.labels(self.name, 'gpio').set(m_value)
    
