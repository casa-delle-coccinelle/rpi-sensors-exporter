#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 nelly <nelly@vivobook>
#
# Distributed under terms of the MIT license.

from setuptools import setup

setup(name='rpi_sensors_exporter',
      version='0.0.1',
      description='Raspberry Pi sensors exporter for Prometheus',
      author='Aneliya Ivanova',
      author_email='aneliya.n.ivanova@gmail.com',
      url='https://github.com/casa-delle-coccinelle/rpi-sensors-exporter/',
      license = 'MIT',
      install_requires=[
          'adafruit_ads1x15>=1.0.2', 
          'Adafruit_Blinka>=7.1.1', 
          'Adafruit_BMP==1.5.4', 
          'adafruit_circuitpython_ads1x15>=2.2.12', 
          'adafruit_circuitpython_bh1750>=1.0.7', 
          'bme680>=1.1.1', 
          'Flask>=2.0.3', 
          'gpiozero>=1.6.2', 
          'prometheus_client>=0.13.1', 
          'PyYAML>=6.0', 
          'SI1145==1.0.0', 
          'waitress>=2.1.0'
          ],
      dependency_links=[
          'git+https://github.com/adafruit/Adafruit_Python_BMP.git#egg=Adafruit_BMP-1.5.4', 
          'git+https://github.com/casa-delle-coccinelle/Python_SI1145.git#egg=SI1145-1.0.0'
          ],
      packages=['rpi_sensors_exporter']
     )
