#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .switch import SwitchProperty

tags = ["Button"]


class ButtonProperty(SwitchProperty):
    def __init__(
        self,
        node,
        id="button",
        name="Button",
        settable=False,
        retained=True,
        qos=1,
        unit=None,
        data_type=None,
        data_format=None,
        value="OFF",
        set_value=None,
        tags=tags,
        meta={},
    ):
        super().__init__(
            node,
            id,
            name,
            settable,
            retained,
            qos,
            unit,
            data_type,
            data_format,
            value,
            set_value,
            tags,
            meta,
        )

    def push(self):
        self.value = "ON"
        self.value = "OFF"
