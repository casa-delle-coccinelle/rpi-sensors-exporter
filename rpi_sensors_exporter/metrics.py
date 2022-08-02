from prometheus_client import Gauge

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
        sensor_exporter_info = Gauge("sensor_exporter_info", "Exporter info", ['sensor', 'connection'])
    except (ValueError):
        pass

    if sensor_type == "bme688":
        try:
             temperature = Gauge("temperature_celsius", "Temperature in celsius", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
             pressure = Gauge("pressure_pascals", "Pressure in hectopascals", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
             humidity = Gauge("air_humidity_percent", "Air humidity, %", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
             gas_resistance = Gauge("gas_resistance_ohms", "Air resistence", ['sensor', 'connection'])
        except (ValueError):
            pass
    elif sensor_type == "bmp180":
        try:
            temperature = Gauge("temperature_celsius", "Temperature in celsius", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
             pressure = Gauge("pressure_pascals", "Pressure in hectopascals", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
             altitude = Gauge("altitude_meters", "Altitude in meters", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
             sealevel = Gauge("sealevel_pressure_pascals", "Sea level pressure in hectopascals", ['sensor', 'connection'])
        except (ValueError):
            pass
    elif sensor_type == "gpio":
        try:
            gpio_value = Gauge(metric_type, "sensor activity, 1 - False, 0 - True", ['sensor', 'connection'])
        except (ValueError):
            pass
    elif sensor_type == "ads":
        try:
            percentage = Gauge(metric_type + "_percent", "Percentage of " + metric_type + " depending on calibration data (min_value and max_value)", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
            voltage = Gauge(metric_type + "_voltage", "Output voltage of the sensor", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
            ads_value = Gauge(metric_type + "_value", "Raw output value of the sensor", ['sensor', 'connection'])
        except (ValueError):
            pass
    elif sensor_type == "bh1750":
        try:
            vis_light = Gauge("visible_light_intensity_lux", "Visible light intensity in lux", ['sensor', 'connection'])
        except (ValueError):
            pass
    elif sensor_type == "si1145":
        try:
            vis_light = Gauge("visible_light_intensity_lux", "Visible light intensity in lux", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
            ir_light = Gauge("ir_light_intensity_lux", "Infrared light intensity in lux", ['sensor', 'connection'])
        except (ValueError):
            pass
        try:
            uv_index = Gauge("uv_index", "UV index", ['sensor', 'connection'])
        except (ValueError):
            pass

