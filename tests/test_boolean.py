#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings, mqtt_messages   # noqa: F401


def test_boolean_device():
    switch = homie.device.BooleanDevice(
        name="Test Switch", mqtt_settings=mqtt_settings)

    for _ in range(10):
        time.sleep(0.2)
        switch.update_boolean(True)
        time.sleep(0.2)
        switch.update_boolean(False)
