#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


class MySwitch(homie.device.SwitchDevice):
    def set_switch(self, onoff):
        print(
            f"Received MQTT message to set the switch to {onoff}. "
            + "Must replace this method"
        )
        super().set_switch(onoff)


def test_switch_device():
    switch = MySwitch(name="Test Switch", mqtt_settings=mqtt_settings)

    for _ in range(10):
        time.sleep(1)
        switch.update_switch("ON")
        time.sleep(1)
        switch.update_switch("OFF")
