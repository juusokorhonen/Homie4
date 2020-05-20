#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .float import FloatProperty


class SetpointProperty(FloatProperty):
    def __init__(
        self,
        node,
        id=None,
        name=None,
        settable=True,
        retained=True,
        qos=1,
        unit=None,
        data_type=None,
        data_format=None,
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
