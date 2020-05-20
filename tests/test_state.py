#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from .context import homie, mqtt_settings   # noqa: F401


# states allowed for this device
STATES = "A,B,C,D,E"


class MyState(homie.device.StateDevice):
    def set_state(self, state):
        print(
            f"Received MQTT message to set the state to {state}. Must replace this method"
        )
        super().set_state(state)


def test_state_device():
    state = MyState(
        name="Test State", mqtt_settings=mqtt_settings, state_values=STATES
    )

    for _ in range(10):
        time.sleep(1)
        state.update_state("A")
        time.sleep(1)
        state.update_state("B")
        time.sleep(1)
        state.update_state("G")
