#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


class MyInteger(homie.device.IntegerDevice):
    def set_integer(self, value):
        print(
            f"Received MQTT message to set the integer to {value}. "
            + "Must replace this method"
        )
        MyInteger.set_integer(self, value)


def test_integer_device():
    integer = MyInteger(name="Test Integer", mqtt_settings=mqtt_settings)

    for _ in range(10):
        integer.update_value(0)
        time.sleep(1)
        integer.update_value(10)
        time.sleep(1)
        integer.update_value(20)
        time.sleep(1)
