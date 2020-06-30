#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List
from ..helpers import RepeatingTimer


@dataclass
class DeviceState():
    instance_count: int = 0
    devices: List = field(default_factory=list)
    repeating_timer: RepeatingTimer = field(default=None)


device_states = DeviceState()


def generate_device_id(instance_id: int):
    """Generates a device id from instance number.

    Parameters
    ----------
    instance_id : int
        A unique number that defines this instance.

    Returns
    -------
    device_id : str
        Example, 'device0001' for instance 1.

    """
    assert instance_id >= 0 and instance_id < 10000,\
        "Instance number over range"
    return "device{:04d}".format(int(instance_id))
