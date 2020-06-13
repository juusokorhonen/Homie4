#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseDevice
from ..node import BaseNode
from ..node.property import SpeedProperty
import logging

logger = logging.getLogger(__name__)


class SpeedDevice(BaseDevice):
    def __init__(
        self,
        device_id=None,
        name=None,
        homie_settings=None,
        mqtt_settings=None,
        speeds="OFF,LOW,MEDIUM,HIGH",
    ):

        super().__init__(device_id, name, homie_settings=homie_settings,
                         mqtt_settings=mqtt_settings)

        node = BaseNode(self, id="speed", name="Speed", type_="speed")
        self.add_node(node)

        self.speed_property = SpeedProperty(
            node, data_format=speeds, set_value=self.set_speed
        )
        node.add_property(self.speed_property)

        self.start()

    def update_speed(self, speed):
        self.speed_property.value = speed
        logger.debug("Speed Update {}".format(speed))

    def set_speed(self, speed):
        logger.debug("Speed Set {}".format(speed))

#    def publish_homeassistant(self):
#        hass_config = f'homeassistant/fan/{self.device_id}/config'
#        hass_payload = f'{{"name": "{self.name}","command_topic": "homie/{self.device_id}/speed/speed/set","state_topic": "homie/{self.device_id}/speed/speed"}}'

#        super().publish_homeassistant(hass_config,hass_payload)
