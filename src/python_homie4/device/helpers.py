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
