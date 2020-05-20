#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


def test_temperature_humidity_device():
    temp_hum = homie.device.TemperatureHumidityDevice(
        name="Test Temp Hum", mqtt_settings=mqtt_settings)

    for _ in range(10):
        temp_hum.update_temperature(50)
        temp_hum.update_humidity(10)
        time.sleep(1)
        temp_hum.update_temperature(10)
        temp_hum.update_humidity(30)
        time.sleep(1)
        temp_hum.update_temperature(90)
        temp_hum.update_humidity(90)
        time.sleep(1)
