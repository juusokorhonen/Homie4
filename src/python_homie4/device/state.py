#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseDevice
from ..node import StateNode
import logging

logger = logging.getLogger(__name__)


class StateDevice(BaseDevice):
    def __init__(
        self,
        device_id=None,
        name=None,
        homie_settings=None,
        mqtt_settings=None,
        state_values=None,
    ):

        super().__init__(device_id, name, homie_settings, mqtt_settings)

        self.add_node(
            StateNode(
                self,
                id="state",
                name="State",
                state_values=state_values,
                set_state=self.set_state,
            )
        )

        self.start()

    def update_state(self, state):
        self.get_node("state").update_state(state)
        logger.debug("State Update {}".format(state))

    def set_state(self, state):  # received commands from clients
        # subclass must override and provide logic to set the device
        logger.debug("State Set {}".format(state))
