#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .enum import EnumProperty


class SpeedProperty(EnumProperty):
    def __init__(
        self,
        node,
        id="speed",
        name="Speed",
        settable=True,
        retained=True,
        qos=1,
        unit=None,
        data_type="enum",
        data_format="OFF,LOW,MEDIUM,HIGH",
        value=None,
        set_value=None,
        tags=[],
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
