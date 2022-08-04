import yaml
import os
import argparse


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
    else:
        try:
            with open(os.environ['SENSORS_EXPORTER_CONFIG']) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except (KeyError):
            pass
        

    if args.port:
        port = args.port
    else:
        port = os.getenv('SENSORS_EXPORTER_PORT')

    return port, config


