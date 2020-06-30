#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseNode
from ..property import SwitchProperty


class SwitchNode(BaseNode):
    def __init__(
        self,
        device,
        id="switch",
        name="Switch",
        type_="switch",
        retain=True,
        qos=1,
        set_switch=None,
    ):
        super().__init__(device, id, name, type_, retain, qos)

        assert set_switch  # must provide a function to set the value of the switch

        self.add_property(SwitchProperty(self, set_value=set_switch))

    def update_switch(self, onoff):
        self.get_property("switch").value = onoff
