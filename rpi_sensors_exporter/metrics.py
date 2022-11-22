import logging

from prometheus_client import Gauge


def initializeMetrics(sensor_type=None, metric_type=None):
    """ Globally initializes Prometheus metrics, depending on the sensor type.

    Keyword arguments:
        sensor_type - (optional) The type of the sensor for which metrics should be initialized. Supported are bmp180, bme688, gpio, ads1115, bh1750 and si1145
        metric_type - (optional) The metric type, provided by adc and gpio sensors. Will be used in metrics name
    """
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
    global amb_light
    global uv_index

    logger = logging.getLogger(__name__)

    if not sensor_type:
        try:
            logger.debug('Initializing exporter info metric')
            sensor_exporter_info = Gauge("sensor_exporter_info", "Exporter info", ['sensor', 'connection'])
            logger.debug('Exporter info metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
    elif sensor_type == "bme688":
        try:
            logger.debug('Initializing temperature metric')
            temperature = Gauge("temperature_celsius", "Temperature in celsius", ['sensor', 'connection'])
            logger.debug('Temperature metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug('Initializing pressure metric')
            pressure = Gauge("pressure_pascals", "Pressure in hectopascals", ['sensor', 'connection'])
            logger.debug('Pressure metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug('Initializing air humidity metric')
            humidity = Gauge("air_humidity_percent", "Air humidity, %", ['sensor', 'connection'])
            logger.debug('Air humidity metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug('Initializing gas resistance metric')
            gas_resistance = Gauge("gas_resistance_ohms", "Air resistence", ['sensor', 'connection'])
            logger.debug('Gas resistance metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
    elif sensor_type == "bmp180":
        try:
            logger.debug('Initializing temperature metric')
            temperature = Gauge("temperature_celsius", "Temperature in celsius", ['sensor', 'connection'])
            logger.debug('Temperature metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug('Initializing pressure metric')
            pressure = Gauge("pressure_pascals", "Pressure in hectopascals", ['sensor', 'connection'])
            logger.debug('Pressure metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:  
            logger.debug('Initializing altitude metric')
            altitude = Gauge("altitude_meters", "Altitude in meters", ['sensor', 'connection'])
            logger.debug('Altitude metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug('Initializing sealevel pressure metric')
            sealevel = Gauge("sealevel_pressure_pascals", "Sea level pressure in hectopascals", ['sensor', 'connection'])
            logger.debug('Sealevel pressure metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
    elif sensor_type == "gpio":
        try:
            logger.debug(f'Initializing {metric_type} metric')
            gpio_value = Gauge(metric_type, "sensor activity, 1 - False, 0 - True", ['sensor', 'connection'])
            logger.debug(f'{metric_type} metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
    elif sensor_type == "ads1115":
        try:
            logger.debug(f'Initializing {metric_type} percent metric')
            percentage = Gauge(metric_type + "_percent", "Percentage of " + metric_type + " depending on calibration data (min_value and max_value)", ['sensor', 'connection'])
            logger.debug(f'{metric_type} percentage metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug(f'Initializing {metric_type} voltage metric')
            voltage = Gauge(metric_type + "_voltage", "Output voltage of the sensor", ['sensor', 'connection'])
            logger.debug(f'{metric_type} voltage metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug(f'Initializing {metric_type} raw value metric')
            ads_value = Gauge(metric_type + "_value", "Raw output value of the sensor", ['sensor', 'connection'])
            logger.debug(f'{metric_type} raw value metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
    elif sensor_type == "bh1750":
        try:
            logger.debug('Initializing visible light metric')
            amb_light = Gauge("ambient_light_intensity_lux", "Ambient light intensity in lux", ['sensor', 'connection'])
            logger.debug('Visible light metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
    elif sensor_type == "ltr390":
        try:
            logger.debug('Initializing visible light metric')
            amb_light = Gauge("ambient_light_intensity_lux", "Ambient light intensity in lux", ['sensor', 'connection'])
            logger.debug('Visible light metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')
        try:
            logger.debug('Initializing UV index metric')
            uv_index = Gauge("uv_index", "UV index", ['sensor', 'connection'])
            logger.debug('UV index metric initialized successfully')
        except (ValueError):
            logger.debug('Metric already initialized')

