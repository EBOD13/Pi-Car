import os
import logging
from flask import current_app as app
from time import sleep

def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20

def read_temp(ds18b20):
    location = f'/sys/bus/w1/devices/{ds18b20}/w1_slave'
    with open(location) as tfile:
        text = tfile.read()
    secondline = text.split("\n")[1]
    temperature_data = secondline.split(" ")[9]
    temperature = float(temperature_data[2:])/ 1000
    return temperature

class Sensors:
    @staticmethod
    def get_current_temp():
        """
        Safely read the current temperature.
        :return: Dictionary with Celsius and Fahrenheit temperature.
        """
        app.logger.info("Starting to read temperature sensor")

        try:
            ds18b20 = sensor()
            temperature = read_temp(ds18b20)
        except TypeError as e:
            app.logger.warning(f"Unable to use primary temperature sensor in this environment: {e}")
            temperature = 0

        app.logger.info("Finishing reading temperature sensor")
        app.logger.debug(f"Temperature: {temperature}")
        return int(temperature)