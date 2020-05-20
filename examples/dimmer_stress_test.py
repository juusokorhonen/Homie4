#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import logging
import time
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', "src")))
from python_homie4.device import DimmerDevice   # noqa: E402


mqtt_settings = {
    'MQTT_BROKER': os.getenv('mqtt_broker', 'localhost'),
    'MQTT_PORT': int(os.getenv('mqtt_port', 1883)),
    'MQTT_SHARE_CLIENT': False,
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

dimmers = []


class MyDimmer(DimmerDevice):
    def set_dimmer(self, percent):
        print(f'Received MQTT message to set the dimmer to {percent}. "
              + "Must replace this method')


try:
    for x in range(5):
        dimmer = MyDimmer(name='Test Dimmer {}'.format(x),
                          mqtt_settings=mqtt_settings)
        dimmers.append(dimmer)

    while True:
        time.sleep(5)
        for dimmer in dimmers:
            dimmer.update_dimmer(50)
        time.sleep(5)
        for dimmer in dimmers:
            dimmer.update_dimmer(100)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")
