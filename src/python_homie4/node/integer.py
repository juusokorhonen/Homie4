#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseNode
from .property import IntegerProperty


class IntegerNode(BaseNode):
    def __init__(
        self,
        device,
        id="integer",
        name="State",
        type_="integer",
        retain=True,
        qos=1,
        set_value=None,
    ):
        super().__init__(device, id, name, type_, retain, qos)

        assert set_value

        self.add_property(
            IntegerProperty(self, "integer", "Integer", set_value=set_value)
        )

    def update_value(self, value):
        self.get_property("integer").value = value
