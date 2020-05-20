#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie   # noqa: F401

mqtt_settings = {
    "MQTT_BROKER": "localhost",
    "MQTT_PORT": 1883,
}


class MyDimmer(homie.device.DimmerDevice):
    def set_dimmer(self, percent):
        print(
            f"Received MQTT message to set the dimmer to {percent}."
            + "Must replace this method"
        )
        super().set_dimmer(percent)


def test_dimmer_device():
    dimmer = MyDimmer(
        name="Test Dimmer", device_id="testdimmer", mqtt_settings=mqtt_settings
    )

    for _ in range(10):
        dimmer.update_dimmer(0)
        time.sleep(1)
        dimmer.update_dimmer(50)
        time.sleep(1)
        dimmer.update_dimmer(100)
        time.sleep(1)
