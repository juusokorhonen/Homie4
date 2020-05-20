#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseDevice
from ..node import BooleanNode
import logging

logger = logging.getLogger(__name__)


class BooleanDevice(BaseDevice):
    def __init__(
        self, device_id=None, name=None, homie_settings=None, mqtt_settings=None
    ):
        super().__init__(device_id, name, homie_settings, mqtt_settings)

        self.add_node(BooleanNode(self, id="boolean",
                                  set_boolean=self.set_boolean))

        self.start()

    def update_boolean(self, boolean):  # sends updates to clients
        self.get_node("boolean").update_boolean(boolean)
        logger.debug("Boolean Update {}".format(boolean))

    def set_boolean(self, boolean):  # received commands from clients
        logger.debug("Boolean Set {}".format(boolean))
