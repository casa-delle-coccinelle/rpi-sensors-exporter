import os
import argparse
import logging
import sys

import yaml

from typing import Dict, Callable
from schema import Schema, And, Optional, SchemaError

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """ Parse command line arguments. """

    parser = argparse.ArgumentParser(
        prog="rpi_sensors_exporter", description='Raspberry Pi sensors exporter for Prometheus'
    )
    parser.add_argument("-p", "--port", help="Port to bind to", type=int)
    parser.add_argument(
        "-c", "--config_file", help="Path to exporter's configuration file"
    )
    parser.add_argument(
        "-v", "--verbose", help="Enables INFO logs on stdout", action='store_true'
    )
    parser.add_argument(
        "-d", "--debug", help="Enables INFO and DEBUG logs on stdout", action='store_true'
    )
    args = parser.parse_args()
    return args


def logs_setup():
    """ Sets the log level depending on the provided arguments. """

    args = parse_args()
    logger = logging.getLogger(__name__.split('.')[0])

    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)


def validate(config: Dict, conf_fpath: str = ""):
    """ Validates configuration file format. """
    gpio_min = 0
    gpio_max = 27
    analog_in_min = 0
    analog_in_max = 3

    schema = Schema(
        {
            Optional('gpio_devices'): [
                {
                    'name': str,
                    'type': str,
                    'pin': And(
                        int,
                        lambda n: gpio_min <= n <= gpio_max, error=f'Pin number should be between {gpio_min} and {gpio_max}'
                    )
                }
            ],
            Optional('ads_devices'): [
                {
                    'name': str,
                    'type': str,
                    'analog_in': And(int, lambda n: analog_in_min <= n < analog_in_max, error=f'Analog input number should be between {analog_in_min} and {analog_in_max}'),
                    Optional('max_value'): And(
                        int,
                        lambda n: n > analog_in_min, error=f'max_value should be above {analog_in_min}'
                    ),
                    Optional('min_value'): And(
                        int, lambda n: n > 0, error='min_value should be above 0'
                    )
                }
            ]
        })

    logger.info(f'Validating configurations in file {conf_fpath}')
    try:
        schema.validate(config)
    except (SchemaError) as exc:
        raise SchemaError(f'Configuration file {conf_fpath} invalid') from exc
    logger.info('Configuration file format - OK')


def unique_item_check(
    items: list[str],
    err_message: str,
    ok_message: str,
    exception: Callable = ValueError,
    ok_messenger: Callable = logger.debug,
    un_constraint: int = 1
):
    """
    Checks uniqueness of items in a list
    Raises provided exception type when item occurs more than un_constraint times
    """

    for item in items:
        if items.count(item) > un_constraint:
            raise exception(err_message.format(item, items, un_constraint))
        else:
            ok_messenger(ok_message.format(item, items, un_constraint))


def gpio_names_check(device_names: list[str]):
    """ Check if GPIO device names are unique """
    unique_item_check(
        device_names,
        'Device name {} is NOT unique in GPIO devices config, please check your configuration',
        'Device name {} is unique in GPIO devices config',
    )


def gpio_pins_check(device_pins: list[str]):
    """ Check if GPIO device pins are unique """
    unique_item_check(
        device_pins,
        'PIN {} is NOT unique in GPIO devices config, please check your configuration',
        'PIN {} is unique in GPIO devices config'
    )


def gpio_dev_check(config: Dict):
    """
    Check GPIO devices configuration.
    Raises ValueError if device is missconfigured.
    Otherwise passes silently.
    """

    logger.debug('Checking GPIO devices configuration')

    gpio_devices_names = []
    gpio_devices_pins = []

    if 'gpio_devices' not in config:
        logger.debug(
            'There is no configuration provided for GPIO devices, skipping verification'
        )
        return

    for device in config['gpio_devices']:
        if isinstance(device, dict):
            if all([
                'name' in device,
                'pin' in device
            ]):
                gpio_devices_names.append(device['name'])
                gpio_devices_pins.append(device['pin'])
                continue

        raise ValueError(
            f"GPIO Device {device} missconfigured."
        )

    gpio_names_check(device_names=gpio_devices_names)
    gpio_pins_check(device_pins=gpio_devices_pins)


def ads_names_check(device_names: list[str]):
    """ Check if ADS device names are unique """
    unique_item_check(
        device_names,
        'Device name {} is NOT unique in ADS devices config, please check your configuration',
        'Device name {} is unique in ADS devices config',
    )


def ads_check_device(device: Dict) -> str:
    """ Checks ADS dev """
    if isinstance(device, dict):
        if any([
            'name' not in device,
            'input' not in device,
        ]):
            raise ValueError(
                f"ADS Device {device} missconfigured"
            )
        if any([
            'min_value' not in device,
            'max_value' not in device,
        ]):
            logger.debug(
                f"Min and max values are NOT configured for sensor {device['name']}, skipping values verification"
            )
        elif device['min_value'] >= device['max_value']:
            raise ValueError(
                f"min_value can not be bigger or equal to max_value for sensor {device['name']}"
            )
        logger.debug(
            f"min_value and max_value configuration for sensor {device['name']} is valid"
        )
    return device['name']


def ads_dev_check(config: Dict):
    """
    Check ADS devices configuration.
    Raises ValueError if device is missconfigured.
    Otherwise passes silently.
    """

    logger.debug('Checking ADS devices configuration')

    ads_devices_names = []

    if 'ads_devices' not in config:
        logger.debug(
            'There is no configuration provided for ADS devices, skipping verification'
        )
        return

    for device in config['ads_devices']:
        try:
            ads_devices_names.append(ads_dev_check(device))
        except (ValueError) as exc:
            raise ValueError("ADS Devices missconfigured.") from exc
    ads_names_check(device_names=ads_devices_names)


def data_check(config: Dict):
    """ Validates configuration file data for ADS and GPIO devices """

    try:
        gpio_dev_check(config)
        ads_dev_check(config)
    except (ValueError) as exc:
        raise ValueError("Configured devices not as expected.") from exc


def load() -> tuple[int, Dict]:
    """ Loads exporter's configuration. """

    config = {}
    port = 0
    f_path = ""

    args = parse_args()

    if args.config_file:
        logger.info(f'Configuration file {args.config_file} is provided in command line')
        f_path = args.config_file
    else:
        logger.info('No configuration file is provided, checking environment')
        try:
            f_path = os.environ['SENSORS_EXPORTER_CONFIG']
            logger.info(f'Validating configurations in file {args.config_file}')
        except (KeyError):
            logger.info('No configuration was found, assuming only I2C sensors are connected')
            f_path = None

    if f_path:
        with open(f_path) as file_stream:
            config = dict(yaml.load(file_stream, Loader=yaml.FullLoader))
            validate(config)
            data_check(config)
            logger.info('Configuration file data - OK')
            logger.info(
                f'Validation is successful, starting with conf {args.config_file}'
            )

    if args.port:
        logger.info(f'Port {args.port} is provided in command line')
        port = args.port
    else:
        try:
            port = os.environ['SENSORS_EXPORTER_PORT']
            logger.info(f'Port {port} was found in environment')
        except (KeyError):
            logger.info('No port configuration found, will use the default one')

    try:
        port = int(args.port)
    except (ValueError) as exc:
        logger.error(f'Port {args.port} is not a valid port number, will use default')
        logger.error(exc)
        port = 0

    return port, config
