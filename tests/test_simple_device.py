#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import pytest
from .context import homie, mqtt_settings, mqtt_messages   # noqa: F401


def test_simple_device():
    """Tests the basic functionality of a SimpleDevice instance.
    """
    with pytest.raises(AssertionError):
        # Need to provide device_id and name
        homie.device.SimpleDevice(mqtt_settings=mqtt_settings)

    with pytest.raises(AssertionError):
        homie.device.SimpleDevice("simple-device-1",
                                  "Simple Integer Device",
                                  node="integer",
                                  mqtt_settings=mqtt_settings)  # set_value is missing

    initial_value = 10
    device_1 = homie.device.SimpleDevice("simple-device-1",
                                         "Simple Integer Device",
                                         node="integer",
                                         node_init=dict(
                                             set_value=initial_value
                                         ),
                                         mqtt_settings=mqtt_settings)

    assert device_1.get_integer() == initial_value

    # for _ in range(10):
    #     time.sleep(0.2)
    #     switch.update_boolean(True)
    #     time.sleep(0.2)
    #     switch.update_boolean(False)