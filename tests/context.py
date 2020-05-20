#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', "src")))

import python_homie4 as homie   # noqa: E402

mqtt_settings = {
    "MQTT_BROKER": os.getenv("mqtt_broker", "localhost"),
    "MQTT_PORT": int(os.getenv("mqtq_port", 1883)),
}

__all__ = (
    homie,
    mqtt_settings,
)
