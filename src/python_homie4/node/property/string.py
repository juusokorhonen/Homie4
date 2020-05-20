#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseProperty


class StringProperty(BaseProperty):
    def __init__(
        self,
        node,
        id,
        name,
        settable=False,
        retained=True,
        qos=1,
        unit=None,
        data_type="string",
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
            "string",
            data_format,
            value,
            set_value,
            tags,
            meta,
        )
