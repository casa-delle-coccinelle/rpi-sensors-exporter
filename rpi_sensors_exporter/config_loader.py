import os
import argparse
import logging
import sys

import yaml
from schema import Schema, And, Optional, SchemaError, Hook

logger = logging.getLogger("sensors_exporter")


def parse_args():
    """ Parse command line arguments. """

    parser = argparse.ArgumentParser(prog="rpi_sensors_exporter", description='Raspberry Pi sensors exporter for Prometheus')
    parser.add_argument("-p", "--port", help="Port to bind to", type=int)
    parser.add_argument("-c", "--config_file", help="Path to exporter's configuration file")
    parser.add_argument("-v", "--verbose", help="Enables INFO logs on stdout", action='store_true')
    parser.add_argument("-d", "--debug", help="Enables INFO and DEBUG logs on stdout", action='store_true')

    args = parser.parse_args()
    return args


def logs_setup():
    """ Sets the log level depending on the provided arguments. """

    args = parse_args()

    logging.basicConfig(stream=sys.stdout, format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)


def load():
    """ Loads exporter's configuration. """

    config = None
    port = None

    args = parse_args()

    if args.config_file:
        logger.info(f'Configuration file {args.config_file} is provided in command line')
        with open(args.config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logger.info(f'Validating configurations in file {args.config_file}')
            validate(config)
            logger.info(f'Configuration file format - OK')
            data_check(config)
            logger.info(f'Configuration file data - OK')
            logger.info(f'Validation is successful, exporter will be started with config from {args.config_file}')
    else:
        logger.info('No configuration file is provided, checking environment')
        try:
            with open(os.environ['SENSORS_EXPORTER_CONFIG']) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                validate(config)
                logger.info(f'A valid configuration file was found in environment, exporter will be started with configuration from file {f.name}')
        except (KeyError):
            logger.info('No configuration was found, assuming only I2C sensors are connected')
        
    if args.port:
        logger.info(f'Port {args.port} is provided in command line')
        port = args.port
    else:
        try:
            port = os.environ['SENSORS_EXPORTER_PORT']
            logger.info(f'Port {port} was found in environment')
        except (KeyError):
            logger.info('No port configuration found, will use the default one')

    return port, config


def validate(config):
    """ Validates configuration file format. """

    schema = Schema(
            {
                Optional('gpio_devices'): [{'name': str, 'type': str, 'pin': And(int, lambda n: 0 <= n < 28, error='Pin number should be between 0 and 27')}],
                Optional('ads_devices'): [{'name': str, 'type': str, 'analog_in': And(int, lambda n: 0 <= n < 4, error='Analog input number should be between 0 and 3'), Optional('max_value'): And(int, lambda n: n > 0, error='max_value should be above 0'), Optional('min_value'): And(int, lambda n: n > 0, error='min_value should be above 0')}]
                })

    schema.validate(config)

def data_check(config):
    """ Validates configuration file data for ADS and GPIO devices """

    gpio_devices_names = []
    gpio_devices_pins = []
    ads_devices_names = []

    try:
        logger.debug('Checking GPIO devices configuration')
        for device in config['gpio_devices']:
            gpio_devices_names.append(device['name'])
            gpio_devices_pins.append(device['pin'])
        for device_name in gpio_devices_names:
            if gpio_devices_names.count(device_name) > 1:
                raise ValueError(f'Device name {device_name} is NOT unique in GPIO devices config, please check your configuration')
            else:
                logger.debug(f'Device name {device_name} is unique in GPIO devices config')
        for device_pin in gpio_devices_pins:
            if gpio_devices_pins.count(device_pin) > 1:
                raise ValueError(f'PIN {device_pin} is NOT unique in GPIO devices config, please check your configuration')
            else:
                logger.debug(f'PIN {device_pin} is unique in GPIO devices config')
    except (KeyError, AttributeError, TypeError):
        logger.debug('There is no configuration provided for GPIO devices, skipping verification')

    try:
        logger.debug('Checking ADS devices configuration')
        for device in config['ads_devices']:
            logger.debug(f"Validating configuration data for ADS sensor {device['name']}")
            ads_devices_names.append(device['name'])
            try:
                if device['min_value'] >= device['max_value']:
                    raise ValueError(f"min_value can not be bigger or equal to max_value for sensor {device['name']}")
                else:
                    logger.debug(f"min_value and max_value configuration for sensor {device['name']} is valid")
            except (KeyError):
                logger.debug(f"Min and max values are NOT configured for sensor {device['name']}, skipping values verification")
        for device_name in ads_devices_names:
            if ads_devices_names.count(device_name) > 1:
                raise ValueError(f'{device_name} is NOT unique in ADS devices config, please check your configuration')
            else:
                logger.debug(f'{device_name} is unique in ADS devices config')
    except (KeyError, AttributeError, TypeError):
        logger.debug('There no configuration provided for ADS devices, skipping verification')

