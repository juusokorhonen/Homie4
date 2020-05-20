#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseDevice
from ..node import BaseNode
from ..node.property import ButtonProperty
import logging

logger = logging.getLogger(__name__)


class ButtonDevice(BaseDevice):
    def __init__(
        self,
        device_id=None,
        name=None,
        homie_settings=None,
        mqtt_settings=None,
    ):

        super().__init__(device_id, name, homie_settings, mqtt_settings)

        node = BaseNode(self, "button", "Button", "button")
        self.add_node(node)

        self.button = ButtonProperty(
            node,
            id="button",
            name="Button",
        )
        node.add_property(self.button)

        self.start()

    def push_button(self):
        self.button.push()
