import logging

from prometheus_client import Gauge

logger = logging.getLogger("sensors_exporter")

temperature = None
pressure = None 
humidity = None 
gas_resistance = None 
altitude = None
sealevel = None
percentage = None
value = None
voltage = None
sensor_exporter_info = None


def initializeMetrics(sensor_type, metric_type=None):
    global temperature
    global pressure
    global humidity 
    global gas_resistance
    global altitude
    global sealevel
    global gpio_value
    global ads_value
    global percentage
    global voltage
    global sensor_exporter_info
    global vis_light
    global ir_light
    global uv_index

    try:
        logger.debug('Initializing exporter info metric')
        sensor_exporter_info = Gauge("sensor_exporter_info", "Exporter info", ['sensor', 'connection'])
        logger.debug('Exporter info metric initialized successfully')
    except (ValueError):
        logger.debug('Metric already initialized')
        pass

    if sensor_type == "bme688":
        try:
            logger.debug('Initializing temperature metric')
            temperature = Gauge("temperature_celsius", "Temperature in celsius", ['sensor', 'connection'])
            logger.debug('Temperature metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing pressure metric')
            pressure = Gauge("pressure_pascals", "Pressure in hectopascals", ['sensor', 'connection'])
            logger.debug('Pressure metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing air humidity metric')
            humidity = Gauge("air_humidity_percent", "Air humidity, %", ['sensor', 'connection'])
            logger.debug('Air humidity metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing gas resistance metric')
            gas_resistance = Gauge("gas_resistance_ohms", "Air resistence", ['sensor', 'connection'])
            logger.debug('Gas resistance metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
    elif sensor_type == "bmp180":
        try:
            logger.debug('Initializing temperature metric')
            temperature = Gauge("temperature_celsius", "Temperature in celsius", ['sensor', 'connection'])
            logger.debug('Temperature metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing pressure metric')
            pressure = Gauge("pressure_pascals", "Pressure in hectopascals", ['sensor', 'connection'])
            logger.debug('Pressure metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:  
            logger.debug('Initializing altitude metric')
            altitude = Gauge("altitude_meters", "Altitude in meters", ['sensor', 'connection'])
            logger.debug('Altitude metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing sealevel pressure metric')
            sealevel = Gauge("sealevel_pressure_pascals", "Sea level pressure in hectopascals", ['sensor', 'connection'])
            logger.debug('Sealevel pressure metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
    elif sensor_type == "gpio":
        try:
            logger.debug(f'Initializing {metric_type} metric')
            gpio_value = Gauge(metric_type, "sensor activity, 1 - False, 0 - True", ['sensor', 'connection'])
            logger.debug(f'{metric_type} metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
    elif sensor_type == "ads":
        try:
            logger.debug(f'Initializing {metric_type} percent metric')
            percentage = Gauge(metric_type + "_percent", "Percentage of " + metric_type + " depending on calibration data (min_value and max_value)", ['sensor', 'connection'])
            logger.debug(f'{metric_type} percentage metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug(f'Initializing {metric_type} voltage metric')
            voltage = Gauge(metric_type + "_voltage", "Output voltage of the sensor", ['sensor', 'connection'])
            logger.debug(f'{metric_type} voltage metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug(f'Initializing {metric_type} raw value metric')
            ads_value = Gauge(metric_type + "_value", "Raw output value of the sensor", ['sensor', 'connection'])
            logger.debug(f'{metric_type} raw value metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
    elif sensor_type == "bh1750":
        try:
            logger.debug('Initializing visible light metric')
            vis_light = Gauge("visible_light_intensity_lux", "Visible light intensity in lux", ['sensor', 'connection'])
            logger.debug('Visible light metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
    elif sensor_type == "si1145":
        try:
            logger.debug('Initializing visible light metric')
            vis_light = Gauge("visible_light_intensity_lux", "Visible light intensity in lux", ['sensor', 'connection'])
            logger.debug('Visible light metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing infrared light metric')
            ir_light = Gauge("ir_light_intensity_lux", "Infrared light intensity in lux", ['sensor', 'connection'])
            logger.debug('Infrared light metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass
        try:
            logger.debug('Initializing UV index metric')
            uv_index = Gauge("uv_index", "UV index", ['sensor', 'connection'])
            logger.debug('UV index metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
            pass

