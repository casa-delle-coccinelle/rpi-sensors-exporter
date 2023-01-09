from setuptools import setup, find_packages

setup(name='rpi_sensors_exporter',
      version='0.0.1',
      description='Raspberry Pi sensors exporter for Prometheus',
      author='Aneliya Ivanova',
      author_email='aneliya.n.ivanova@gmail.com',
      url='https://github.com/casa-delle-coccinelle/rpi-sensors-exporter/',
      license = 'MIT',
      install_requires=[
          'Adafruit_Blinka>=7.1.1', 
          'Adafruit_BMP @ git+https://github.com/adafruit/Adafruit_Python_BMP@1.5.4#egg=Adafruit_BMP', 
          'adafruit_circuitpython_ads1x15>=2.2.12', 
          'adafruit_circuitpython_bh1750>=1.0.7', 
          'adafruit-circuitpython-ltr390>=1.1.10',
          'adafruit-circuitpython-sht4x>=1.0.15',
          'bme680>=1.1.1', 
          'Flask>=2.0.3', 
          'gpiozero>=1.6.2', 
          'prometheus_client>=0.13.1', 
          'PyYAML>=6.0', 
          'waitress>=2.1.0',
          'schema>=0.7.5'
          ],
      packages=find_packages()
     )
