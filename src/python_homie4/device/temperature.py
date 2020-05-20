#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .status import StatusDevice
from ..node.property import TemperatureProperty
import logging

logger = logging.getLogger(__name__)


class TemperatureDevice(StatusDevice):
    def __init__(
        self,
        device_id=None,
        name=None,
        homie_settings=None,
        mqtt_settings=None,
        temp_units="F",
    ):
        self.temp_units = temp_units

        super().__init__(device_id, name, homie_settings, mqtt_settings)

    def register_status_properties(self, node):
        self.temperature = TemperatureProperty(node, unit=self.temp_units)
        node.add_property(self.temperature)

    def update_temperature(self, temperature):
        logger.info("Updated Temperature {}".format(temperature))
        self.temperature.value = temperature
