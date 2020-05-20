#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


class MyBooleanDevice(homie.device.BooleanDevice):
    def set_switch(self, onoff):
        print(
            f"Received MQTT message to set the switch to {onoff}. "
            + "Must replace this method"
        )
        super().set_switch(onoff)


def test_boolean_device():
    switch = MyBooleanDevice(
        name="Test Switch", mqtt_settings=mqtt_settings)

    # Run once
    time.sleep(1)
    switch.update_boolean(True)
    time.sleep(1)
    switch.update_boolean(False)
