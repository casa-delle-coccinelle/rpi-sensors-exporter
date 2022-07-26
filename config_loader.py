import yaml

try:
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except (FileNotFoundError):
    pass

#print(config)
#
#for gpio in config['gpio_devices']:
#    print(gpio['name'])
#    print(gpio['pin'])
#
#
#for ads in config['ads_devices']:
#    print(ads['name'])
#    print(ads['input'])
#
