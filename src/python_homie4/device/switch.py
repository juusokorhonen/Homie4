#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseDevice
from ..node import SwitchNode
import logging

logger = logging.getLogger(__name__)


class SwitchDevice(BaseDevice):
    def __init__(
        self, device_id=None, name=None, homie_settings=None, mqtt_settings=None
    ):
        super().__init__(device_id, name, homie_settings=homie_settings,
                         mqtt_settings=mqtt_settings)

        self.add_node(SwitchNode(self, id="switch",
                                 set_switch=self.set_switch))

        self.start()

    def update_switch(self, onoff):  # sends updates to clients
        self.get_node("switch").update_switch(onoff)
        logger.debug("Switch Update {}".format(onoff))

    def set_switch(self, onoff):  # received commands from clients
        logger.debug("Switch Set {}".format(onoff))
