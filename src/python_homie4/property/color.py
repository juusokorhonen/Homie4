#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseProperty


class ColorProperty(BaseProperty):
    """
    Notes
    -----
    Not completed
    """

    def __init__(
        self,
        node,
        id,
        name,
        settable=True,
        retained=True,
        qos=1,
        unit=None,
        data_type="color",
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
            "color",
            data_format,
            value,
            set_value,
            tags,
            meta,
        )

        # check valid data format provided

    def message_handler(self, topic, payload):
        pass
