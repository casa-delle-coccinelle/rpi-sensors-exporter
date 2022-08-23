import os
import argparse
import logging
import sys

import yaml
from schema import Schema, And, Optional, SchemaError

logging.basicConfig(stream=sys.stdout, format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__name__)


def load():
    config = None
    port = None

    parser = argparse.ArgumentParser(prog="rpi_sensors_exporter", description='Raspberry Pi sensors exporter for Prometheus')
    parser.add_argument("-p", "--port", help="Port to run the exporter", type=int)
    parser.add_argument("-c", "--config_file", help="Path to exporter's configuration file")

    args = parser.parse_args()


    if args.config_file:
        logger.info('Configuration file ' + str(args.config_file) + ' is provided in command line')
        with open(args.config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logger.info('Validating configurations in file ' + str(args.config_file))
            validate(config)
            logger.info('Validation is successful, exporter will be started with config from '  + str(args.config_file))
    else:
        logger.info('No configuration file is provided, checking environment')
        try:
            with open(os.environ['SENSORS_EXPORTER_CONFIG']) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                validate(config)
                logger.info('A valid configuration file was found in environment, exporter will be started with config from ' + str(os.environ['SENSORS_EXPORTER_CONFIG']))
        except (KeyError):
            logger.info('No configuration was found, assuming only I2C sensors are connected')
            pass
        

    if args.port:
        logger.info('Port ' + str(args.port) + ' is provided in command line')
        port = args.port
    else:
        try:
            port = os.environ['SENSORS_EXPORTER_PORT']
            logger.info('Port ' + str(port) + ' was found in environment')
        except (KeyError):
            logger.info('No port configuration found, will use the default one')
            pass

    return port, config


def validate(config):

    schema = Schema(
            {
                Optional('gpio_devices'): [{'name': str, 'type': str, 'pin': And(int, lambda n: 0 <= n < 28, error='Pin number should be between 0 and 27')}],
                Optional('ads_devices'): [{'name': str, 'type': str, 'analog_in': And(int, lambda n: 0 <= n < 4, error='Analog input number should be between 0 and 3'), Optional('max_value'): int, Optional('min_value'): int}]
                })

    schema.validate(config)

