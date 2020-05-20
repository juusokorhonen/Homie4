#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


def test_contact_device():
    contact = homie.device.ContactDevice(
        name="Test Contact", device_id="testcontact", mqtt_settings=mqtt_settings
    )

    for _ in range(10):
        time.sleep(1)
        contact.update_contact("OPEN")
        time.sleep(1)
        contact.update_contact("CLOSED")
