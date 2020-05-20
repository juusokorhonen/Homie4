#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


THERMOSTAT_SETTINGS = {
    "current_temperature": 70,
    "current_humidity": 30,
    "cool_setpoint": 70,
    "max_cool_setpoint": 90,
    "min_cool_setpoint": 60,
    "heat_setpoint": 70,
    "max_heat_setpoint": 90,
    "min_heat_setpoint": 60,
    "fan_mode": "ON",
    "fan_modes": ["ON", "AUTO"],
    "hold_mode": "SCHEDULE",
    "hold_modes": ["SCHEDULE", "TEMPORARY", "PERMANENT"],
    "system_mode": "OFF",
    "system_modes": ["OFF", "HEAT", "COOL", "AUTO"],
    "system_status": "OFF",
    "units": "F",
}


def test_thermostat_device():
    therm = homie.device.ThermostatDevice(
        name="Thermostat",
        mqtt_settings=mqtt_settings,
        thermostat_settings=THERMOSTAT_SETTINGS,
    )

    for _ in range(10):
        therm.update_current_temperature(60)
        therm.update_current_humidity(10)
        therm.update_heat_setpoint(70)
        therm.update_cool_setpoint(80)
        time.sleep(1)
        therm.update_current_temperature(66)
        therm.update_current_humidity(30)
        therm.update_heat_setpoint(75)
        therm.update_cool_setpoint(85)
        time.sleep(1)
