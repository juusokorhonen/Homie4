#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseProperty


class EnumProperty(BaseProperty):
    def __init__(
        self,
        node,
        id,
        name,
        settable=True,
        retained=True,
        qos=1,
        unit=None,
        data_type="enum",
        data_format=None,
        value=None,
        set_value=None,
        tags=[],
        meta={},
    ):
        assert data_format
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

        self.enum_list = data_format.split(",")

    def validate_value(self, value):
        return value in self.enum_list
