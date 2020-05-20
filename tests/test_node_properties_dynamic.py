#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import logging
from .context import homie, mqtt_settings   # noqa: F401

logger = logging.getLogger(__name__)


class MyContactDevice(homie.device.BaseDevice):
    def __init__(
        self, device_id=None, name=None, homie_settings=None, mqtt_settings=None
    ):

        super().__init__(device_id, name, homie_settings, mqtt_settings)

        self.add_node(homie.node.ContactNode(self, id="contact"))

        self.start()

    def update_contact(self, state):
        self.get_node("contact").update_contact(state)
        logging.info("Contact Update {}".format(state))


def test_node_properties_dynamic():
    contact = homie.device.ContactDevice(
        name="Test Contact", mqtt_settings=mqtt_settings)

    for _ in range(10):
        time.sleep(1)

        node = contact.get_node("contact")
        node.add_property(homie.node.property.ContactProperty(
            node, id="contactdynamic"))

        contact.update_contact("OPEN")

        time.sleep(1)

        node = contact.get_node("contact")
        node.remove_property("contactdynamic")

        contact.update_contact("CLOSED")
