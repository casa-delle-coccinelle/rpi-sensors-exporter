import logging

import SI1145.SI1145 as SI1145 

from .. import metrics

logger = logging.getLogger("sensors_exporter")

class Metrics:
    sensor = None

    def __init__(self):

        logger.debug('[SI1145] Initializing sensor')
        self.sensor = SI1145.SI1145(i2c_bus=1)
        self.sensor.readProx()

    def __del__(self):
        self.sensor.close()


    def getSensorData(self):

        logger.debug('[SI1145] Reading sensor data')
        _vis = self.sensor.readVisible()
        _IR = self.sensor.readIR()
        _UV = self.sensor.readUV()
        _uvIndex = _UV / 100.0
        
        return (_vis, _IR, _uvIndex)
    
    
    def getMetrics(self):
    
        m_vis, m_IR, m_uvIndex = self.getSensorData()
        logger.debug('[SI1145] Populating metrics')

        return metrics.vis_light.labels("si1145", "i2c").set(m_vis), metrics.ir_light.labels("si1145", "i2c").set(m_IR), metrics.uv_index.labels("si1145", "i2c").set(m_uvIndex)
