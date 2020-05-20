#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .integer import IntegerProperty

tags = ["Lighting", "Dimmable"]


class DimmerProperty(IntegerProperty):
    def __init__(
        self,
        node,
        id="dimmer",
        name="Dimmer",
        settable=True,
        retained=True,
        qos=1,
        unit="%",
        data_type=None,
        data_format="0:100",
        value=None,
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
