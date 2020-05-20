#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseNode
from .property import DimmerProperty


class DimmerNode(BaseNode):
    def __init__(
        self,
        device,
        id="dimmer",
        name="Dimmer",
        type_="dimmer",
        retain=True,
        qos=1,
        set_dimmer=None,
    ):
        super().__init__(device, id, name, type_, retain, qos)

        assert set_dimmer  # must provide a function to set the value of the dimmer

        self.add_property(DimmerProperty(self, set_value=set_dimmer))

    def update_dimmer(self, percent):
        self.get_property("dimmer").value = percent
