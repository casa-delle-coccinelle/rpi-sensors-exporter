import Adafruit_BMP.BMP085 as BMP085 

from .. import metrics


class BMP180Metrics:
    sensor = None

    def __init__(self):
        self.sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

    def getSensorData(self):

        temp = self.sensor.read_temperature()
        press = self.sensor.read_pressure()
        altitude = self.sensor.read_altitude()
        sea_press = self.sensor.read_sealevel_pressure()
        
        return (temp, press, altitude, sea_press)
    
    def getMetrics(self):
        m_temp, m_press, m_alt, m_sea_press = self.getSensorData()
        return metrics.temperature.labels("bmp180", "i2c").set(m_temp), metrics.pressure.labels("bmp180", "i2c").set(m_press * 0.01), metrics.altitude.labels("bmp180", "i2c").set(m_alt), metrics.sealevel.labels("bmp180", "i2c").set(m_sea_press * 0.01)
