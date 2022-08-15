import os
import argparse

import yaml
from schema import Schema, And, Optional, SchemaError


def load():
    config = None
    port = None

    parser = argparse.ArgumentParser(prog="rpi_sensors_exporter", description='Raspberry Pi sensors exporter for Prometheus')
    parser.add_argument("-p", "--port", help="Port to run the exporter", type=int)
    parser.add_argument("-c", "--config_file", help="Path to exporter's configuration file")

    args = parser.parse_args()


    if args.config_file:
        with open(args.config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            validate(config)
    else:
        try:
            with open(os.environ['SENSORS_EXPORTER_CONFIG']) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                validate(config)
        except (KeyError):
            pass
        

    if args.port:
        port = args.port
    else:
        port = os.getenv('SENSORS_EXPORTER_PORT')

    return port, config


def validate(config):

    schema = Schema(
            {
                Optional('gpio_devices'): [{'name': str, 'type': str, 'pin': And(int, lambda n: 0 <= n < 28, error='Pin number should be between 0 and 27')}],
                Optional('ads_devices'): [{'name': str, 'type': str, 'analog_in': And(int, lambda n: 0 <= n < 4, error='Analog input number should be between 0 and 3'), Optional('max_value'): int, Optional('min_value'): int}]
                })

    schema.validate(config)

