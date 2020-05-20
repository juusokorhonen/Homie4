#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .temperature import TemperatureDevice
from ..node.property import HumidityProperty
import logging

logger = logging.getLogger(__name__)


class TemperatureHumidityDevice(TemperatureDevice):
    def register_status_properties(self, node):
        super().register_status_properties(node)

        self.humidity = HumidityProperty(node)
        node.add_property(self.humidity)

    def update_humidity(self, humidity):
        logger.info("Updated Humidity {}".format(humidity))
        self.humidity.value = humidity
