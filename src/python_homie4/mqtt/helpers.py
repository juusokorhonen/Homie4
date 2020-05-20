#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from .paho_mqtt_client import PahoMQTTClient
MQTTClient = PahoMQTTClient

logger = logging.getLogger(__name__)

mqtt_client_count = 0
mqtt_clients = []
common_mqtt_client = None

DEFAULT_MQTT_SETTINGS = {
    "MQTT_BROKER": None,
    "MQTT_PORT": 1883,
    "MQTT_USERNAME": None,
    "MQTT_PASSWORD": None,
    "MQTT_KEEPALIVE": 60,
    "MQTT_CLIENT_ID": None,
    "MQTT_SHARE_CLIENT": False,
}


def validate_mqtt_settings(settings):
    settings = settings.copy()

    for setting, value in DEFAULT_MQTT_SETTINGS.items():
        if setting not in settings:
            settings[setting] = DEFAULT_MQTT_SETTINGS[setting]
        logger.debug("MQTT Settings {} {}".format(setting, settings[setting]))

    assert settings["MQTT_BROKER"]
    assert settings["MQTT_PORT"]

    return settings


def connect_mqtt_client(device, mqtt_settings):
    global mqtt_client_count
    mqtt_settings = validate_mqtt_settings(mqtt_settings)
    mqtt_client = None
    last_will_topic = "/".join((device.topic, "$state"))

    if mqtt_settings["MQTT_SHARE_CLIENT"] is not True:
        logger.info(
            f"Using new MQTT client, number of instances {mqtt_client_count}")

        mqtt_client = MQTTClient(mqtt_settings, last_will_topic)
        mqtt_client.connect()
        mqtt_client_count = mqtt_client_count + 1
        mqtt_clients.append(mqtt_client)
    else:
        logger.info("Using common MQTT client")

        global common_mqtt_client
        if common_mqtt_client is None:
            common_mqtt_client = MQTTClient(mqtt_settings, last_will_topic)
            common_mqtt_client.connect()
            mqtt_client_count = mqtt_client_count + 1
            mqtt_clients.append(mqtt_client)

        mqtt_client = common_mqtt_client

    mqtt_client.add_device(device)

    return mqtt_client


def close_mqtt_clients():
    logger.info('Closing all MQTT clients')
    for client in mqtt_clients:
        client.close()
