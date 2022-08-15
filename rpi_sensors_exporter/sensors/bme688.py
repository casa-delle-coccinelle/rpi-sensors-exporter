import time

import bme680 

from .. import metrics


class BME688Metrics:
    sensor = None

    def __init__(self):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        
        self.sensor.set_gas_heater_temperature(200)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)
        


    def getSensorData(self):
        self.sensor.get_sensor_data()
        _temp = self.sensor.data.temperature
        _press = self.sensor.data.pressure
        _humidity = self.sensor.data.humidity
        for retry in range(5):
           if self.sensor.data.heat_stable:
               _gas_resistance = self.sensor.data.gas_resistance
               break
           else:
               time.sleep(1)
               self.sensor.get_sensor_data()
        
        return (_temp, _press, _humidity, _gas_resistance)
    
    
    def getMetrics(self):
    
        m_temp, m_press, m_hum, m_gas = self.getSensorData()

        return metrics.temperature.labels("bme688", "i2c").set(m_temp), metrics.pressure.labels("bme688", "i2c").set(m_press), metrics.humidity.labels("bme688", "i2c").set(m_hum), metrics.gas_resistance.labels("bme688", "i2c").set(m_gas)
