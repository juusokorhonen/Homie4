#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod
from .base import BaseDevice
from ..node import BaseNode
import logging

logger = logging.getLogger(__name__)


class StatusDevice(BaseDevice):
    def __init__(
        self, device_id=None, name=None, homie_settings=None, mqtt_settings=None
    ):

        super().__init__(device_id, name, homie_settings=homie_settings,
                         mqtt_settings=mqtt_settings)

        node = BaseNode(self, "status", "Status", "status")
        self.add_node(node)

        self.register_status_properties(node)

        self.start()

    @abstractmethod
    def register_status_properties(self, node):
        pass
