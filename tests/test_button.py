#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


def test_button_device():
    button = homie.device.ButtonDevice(
        device_id="button", name="Test Button", mqtt_settings=mqtt_settings)

    for _ in range(10):
        time.sleep(1)
        button.push_button()
        print('button push')
