#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .integer import IntegerProperty


class HumidityProperty(IntegerProperty):
    def __init__(
        self,
        node,
        id="humidity",
        name="Humidity",
        settable=False,
        retained=True,
        qos=1,
        unit="%",
        data_type=None,
        data_format="0:100",
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
