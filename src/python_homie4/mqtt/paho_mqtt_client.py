#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import threading
import functools
import paho.mqtt.client as mqtt_client
from .mqtt_base import MQTTBase

import logging
logger = logging.getLogger(__name__)


class PahoMQTTClient(MQTTBase):
    CONNECTION_RESULT_CODES = {
        0: "Connection successful",
        1: "Connection refused - incorrect protocol version",
        2: "Connection refused - invalid client identifier",
        3: "Connection refused - server unavailable",
        4: "Connection refused - bad username or password",
        5: "Connection refused - not authorised",
    }

    def __init__(self, mqtt_settings, last_will):
        super().__init__(mqtt_settings, last_will)
        self.mqtt_client = None

    def connect(self):
        """Connects to MQTT broker.

        """
        super().connect()

        self.mqtt_client = mqtt_client.Client(
            client_id=self.mqtt_settings["MQTT_CLIENT_ID"],
            protocol=mqtt_client.MQTTv31
            # clean_session=0
        )
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        # self.mqtt_client.on_publish = self._on_publish
        self.mqtt_client.on_disconnect = self._on_disconnect

        self.set_will(self.last_will, "lost", True, 1)

        if self.mqtt_settings["MQTT_USERNAME"]:
            self.mqtt_client.username_pw_set(
                self.mqtt_settings["MQTT_USERNAME"],
                password=self.mqtt_settings["MQTT_PASSWORD"],
            )

        try:
            self.mqtt_client.connect(
                self.mqtt_settings["MQTT_BROKER"],
                port=self.mqtt_settings["MQTT_PORT"],
                keepalive=self.mqtt_settings["MQTT_KEEPALIVE"],
            )

            self.mqtt_client.loop_start()

        except (ValueError, ConnectionRefusedError) as e:
            logger.warning("MQTT Unable to connect to Broker {}".format(e))

        def start():
            try:
                asyncio.set_event_loop(self.event_loop)
                logger.info('Starting Asyincio looping forever')
                self.event_loop.run_forever()
                logger.warning('Event loop stopped')

            except Exception as e:
                logger.error('Error in event loop {}'.format(e))

        self.event_loop = asyncio.new_event_loop()

        logger.info("Starting MQTT publish thread")
        self._ws_thread = threading.Thread(target=start, args=())

        self._ws_thread.daemon = True
        self._ws_thread.start()

    def publish(self, topic, payload, retain, qos):
        super().publish(topic, payload, retain, qos)

        wrapped = functools.partial(lambda: self.mqtt_client.publish(
            topic, payload, retain=retain, qos=qos))

        self.event_loop.call_soon_threadsafe(wrapped)

    def subscribe(self, topic, qos):
        super().subscribe(topic, qos)
        self.mqtt_client.subscribe(topic, qos)

    def unsubscribe(self, topic):
        super().unsubscribe(topic)
        self.mqtt_client.unsubscribe(topic)

    def set_will(self, will, topic, retain, qos):
        super().set_will(will, topic, retain, qos)
        self.mqtt_client.will_set(will, topic, retain, qos)

    def _on_connect(self, client, userdata, flags, rc):
        logger.debug(
            f"MQTT On Connect: Result code {rc}, Flags {flags}")
        self.mqtt_connected = rc == 0

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        super()._on_message(topic, payload, msg.retain, msg.qos)

    def _on_disconnect(self, client, userdata, rc):
        """Handler for disconnect events.

        Notes
        -----
        change this uses the property setter, do not really need to catch this
        in the base class

        """
        self.mqtt_connected = False

        if rc > 0:  # unexpected disconnect
            rc_text = "Unknown result code {}".format(rc)
            if rc in self.CONNECTION_RESULT_CODES:
                rc_text = self.CONNECTION_RESULT_CODES[rc]

            logger.warning(
                f"MQTT Unexpected disconnection {client} {userdata} {rc_text}")
        super()._on_disconnect(rc)

    def close(self):
        super().close()
        self.event_loop.stop()
