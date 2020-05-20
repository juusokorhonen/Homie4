#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .temperature_humidity import TemperatureHumidityDevice
from ..node.property import BatteryProperty
import logging

logger = logging.getLogger(__name__)


class TemperatureHumidityBatteryDevice(TemperatureHumidityDevice):
    def register_status_properties(self, node):
        super().register_status_properties(node)

        self.battery = BatteryProperty(node)
        node.add_property(self.battery)

    def update_battery(self, battery):
        logger.info("Updated Battery {}".format(battery))
        self.battery.value = battery
