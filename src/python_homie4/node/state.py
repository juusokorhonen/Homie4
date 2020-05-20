#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseNode
from .property import EnumProperty


class StateNode(BaseNode):
    def __init__(
        self,
        device,
        id="state",
        name="State",
        type_="state",
        retain=True,
        qos=1,
        state_values=None,
        set_state=None,
    ):
        assert state_values
        assert set_state

        super().__init__(device, id, name, type_, retain, qos)

        self.add_property(
            EnumProperty(
                self, "state", "State", data_format=state_values, set_value=set_state
            )
        )

    def update_state(self, state):
        self.get_property("state").value = state
