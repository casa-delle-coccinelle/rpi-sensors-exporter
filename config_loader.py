import yaml
import os

try:
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except (FileNotFoundError):
    pass

try:
    with open(os.environ['EXPORTER_CONFIG']) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except (KeyError):
    pass

