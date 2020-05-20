#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import logging
from collections import deque
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', "src")))

import python_homie4 as homie   # noqa: E402

mqtt_settings = {
    "MQTT_BROKER": os.getenv("mqtt_broker", "localhost"),
    "MQTT_PORT": int(os.getenv("mqtt_port", 1883)),
    "MQTT_CLIENT_ID": 'pytest_listener',
    "MQTT_PROTOCOL_VERSION": mqtt.MQTTv311 if os.getenv(
        "mqtt_protocol_version") == "v311" else mqtt.MQTTv31,
    "MQTT_USERNAME": os.getenv("mqtt_username"),
    "MQTT_PASSWORD": os.getenv("mqtt_password"),
    "MQTT_CAFILE": os.getenv("mqtt_cafile"),
    "MQTT_CERTFILE": os.getenv("mqtt_certfile"),
    "MQTT_KEYFILE": os.getenv("mqtt_keyfile"),
    "MQTT_TLS_UNSAFE": os.getenv("mqtt_tls_unsafe"),
}

try:
    mqtt_messages = deque()
    mqtt_listener = mqtt.Client(client_id=mqtt_settings.get("MQTT_CLIENT_ID"),
                                protocol=mqtt_settings.get("MQTT_PROTOCOL_VERSION"))   # noqa: E501

    mqtt_listener.on_connect = lambda client, userdata, flags, rc:\
        logger.info("MQTT listener connected")
    mqtt_listener.on_disconnect = lambda client, userdata, rc:\
        logger.info("MQTT listener disconnected.")
    mqtt_listener.on_message = lambda client, userdata, msg:\
        mqtt_messages.append(msg)

    if mqtt_settings.get("MQTT_CAFILE") is not None:
        mqtt_listener.tls_set(
            ca_certs=mqtt_settings.get("MQTT_CAFILE"),
            certfile=mqtt_settings.get("MQTT_CERTFILE"),
            keyfile=mqtt_settings.get("MQTT_KEYFILE"),
            cert_reqs=False if mqtt_settings.get(
                "MQTT_TLS_UNSAFE") else True
        )

    if mqtt_settings["MQTT_USERNAME"]:
        mqtt_listener.username_pw_set(
            mqtt_settings["MQTT_USERNAME"],
            password=mqtt_settings["MQTT_PASSWORD"],
        )

    mqtt_listener.connect(mqtt_settings.get("MQTT_BROKER"),
                          port=mqtt_settings.get("MQTT_PORT"))
    mqtt_listener.subscribe('#')

except ValueError:
    logger.error("MQTT connect failed.")


__all__ = (
    homie,
    mqtt_settings,
    mqtt_listener,
    mqtt_messages,
)
