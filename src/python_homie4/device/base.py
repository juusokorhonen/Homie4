#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
from abc import ABCMeta
from datetime import datetime

from .. import __version__ as fw_version
from .. import __name__ as fw_name
from ..helpers import validate_topic
from ..mqtt.helpers import connect_mqtt_client, close_mqtt_clients
from ..helpers import RepeatingTimer
from .helpers import device_states, generate_device_id
from ..node import BaseNode

import logging
logger = logging.getLogger(__name__)


class BaseDevice(metaclass=ABCMeta):
    """A base class for all devices.

    Notes
    -----
    A 'device' comprises one ore more 'nodes'. Each 'node' contains one or more
    'properties'. For example, a sensor device could be made from a thermometer
    node and an anemometer node. The thermometer node would add a property
    called temperature. The anemometer node could house a wind speed property
    and a wind direction property.

    Nodes are registered to the devie using `add_node` method, which binds
    `update_` and `get_` methods. For example, adding a node called
    "thermometer" will create two methods called `update_thermometer` and
    `get_thermometer`.

    """
    DEVICE_STATES = [
        "init",
        "ready",
        "disconnected",
        "sleeping",
        "alert",
        "lost",
    ]

    DEFAULT_HOMIE_SETTINGS = {
        "version": "4.0.0",
        "topic": "homie",
        "fw_name": fw_name,
        "fw_version": fw_version,
        "update_interval": 60,
        "implementation": sys.platform,
    }

    SUPPORTED_EXTENSIONS = ["stats", "firmware", "meta"]

    SUPPOERTED_EXTENSION_IDENTIFIERS = {
        "stats": "org.homie.legacy-stats:0.1.1:[4.x]",
        "firmware": "org.homie.legacy-firmware:0.1.1:[4.x]",
        "meta": "eu.epnw.meta:1.1.0:[3.0.1;4.x]",
    }

    def __init__(
        self,
        device_id,
        name,
        *,
        homie_settings={},
        mqtt_settings={},
        extensions=["stats", "firmware", "meta"],
    ):
        device_states.instance_count += 1
        self.instance_number = device_states.instance_count

        self._mqtt_connected = False

        if device_id is None:
            device_id = generate_device_id(self.instance_number)

        assert validate_topic(
            device_id), "Invalid device id {}".format(device_id)
        self.device_id = device_id

        assert name
        self.name = name

        for extension in extensions:
            assert extension in self.SUPPORTED_EXTENSIONS
        self.extensions = extensions

        self._state = "init"

        self.homie_settings = self._validate_homie_settings(homie_settings)
        self.topic = "/".join((self.homie_settings["topic"], self.device_id))

        # may need a way to set these
        self.retained = True
        self.qos = 1

        self.nodes = {}
        self.start_time = None
        self.nodes_published = False

        self.mqtt_client = connect_mqtt_client(self, mqtt_settings)
        self.mqtt_subscription_handlers = {}

        device_states.devices.append(self)

    def close(self, *args):
        logger.info("Device Close {}".format(self.name))
        self.state = "disconnected"

    def start(self):
        """Starts the device.

        Notes
        -----
        Called after the device has been built with nodes and properties

        """
        logger.info("Device Start {}".format(self.name))
        self.start_time = time.time()

        if "stats" in self.extensions:
            if device_states.repeating_timer is None:
                device_states.repeating_timer = RepeatingTimer(
                    self.homie_settings["update_interval"]
                )

            device_states.repeating_timer.add_callback(self.publish_uptime)

        if self.mqtt_client.mqtt_connected:
            # run start up tasks if mqtt is ready, else wait for on_connect
            # message from mqtt client
            self.on_mqtt_connection(True)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state, retain=True, qos=1):
        if state in self.DEVICE_STATES:
            self._state = state
            self.publish("/".join((self.topic, "$state")),
                         self._state, retain, qos)
        else:
            logger.warning("Homie Invalid device state {}".format(state))

    def publish_attributes(self, retain=True, qos=1):
        self.publish(
            "/".join((self.topic, "$homie")),
            self.homie_settings["version"],
            retain,
            qos,
        )
        self.publish("/".join((self.topic, "$name")), self.name, retain, qos)
        self.publish(
            "/".join((self.topic, "$implementation")),
            self.homie_settings["implementation"],
            retain,
            qos,
        )

        self.publish_extensions(retain, qos)

        self.state = "ready"

    def publish_extensions(self, retain=True, qos=1):
        extensions = ",".join(self.extensions)

        if extensions != "":
            self.publish("/".join((self.topic, "$extensions")),
                         extensions, retain, qos)

        if "stats" in self.extensions:
            self.publish_statistics(retain, qos)

        if "firmware" in self.extensions:
            self.publish_firmware(retain, qos)

    def publish_firmware(self, retain=True, qos=1):
        mac, ip = self.mqtt_client.get_mac_ip_address()

        self.publish("/".join((self.topic, "$localip")), ip, retain, qos)
        self.publish("/".join((self.topic, "$mac")), mac, retain, qos)
        self.publish("/".join((self.topic, "$fw/name")),
                     self.homie_settings['fw_name'], retain, qos)
        self.publish("/".join((self.topic, "$fw/version")),
                     self.homie_settings['fw_version'], retain, qos)
        self.publish("/".join((self.topic, "$implementation")),
                     self.homie_settings['implementation'], retain, qos)

    def publish_statistics(self, retain=True, qos=1):
        self.publish("/".join((self.topic, "$stats/interval")),
                     self.homie_settings['update_interval'], retain, qos)
        self.publish("/".join((self.topic, "$stats/uptime")),
                     time.time()-self.start_time, retain, qos)
        self.publish("/".join((self.topic, "$stats/lastupdate")),
                     datetime.now().strftime("%d/%m/%Y %H:%M:%S"), retain, qos)

    def publish_uptime(self, retain=True, qos=1):
        self.publish("/".join((self.topic, "$stats/uptime")),
                     time.time()-self.start_time, retain, qos)
        self.publish("/".join((self.topic, "$stats/lastupdate")),
                     datetime.now().strftime("%d/%m/%Y %H:%M:%S"), retain, qos)

    def add_subscription(self, topic, handler, qos=0):
        """Starts a subscription to a topic.

        Notes
        -----
        Subscription list to the required MQTT topics, used by properties to catch set topics

        """
        self.mqtt_subscription_handlers[topic] = handler
        self.mqtt_client.subscribe(topic, qos)
        logger.debug('MQTT subscribed to {}'.format(topic))

    def remove_subscription(self, topic):
        self.mqtt_client.unsubscribe(topic)
        del self.mqtt_subscription_handlers[topic]
        logger.debug('MQTT unsubscribed to {}'.format(topic))

    def subscribe_topics(self):
        logger.debug("Device subscribing to topics")
        self.add_subscription(
            "/".join((self.topic, "$broadcast/#")), self.broadcast_handler
        )  # get the broadcast events

        for _, node in self.nodes.items():
            for topic, handler in node.get_subscriptions().items():
                self.add_subscription(topic, handler)

    def add_node(self, node: BaseNode):
        """Registers a `node` to this device.

        Parameters
        ----------
        node : BaseNode
            An instance of BaseNode to register to this device.

        """
        assert isinstance(node, BaseNode)
        assert node.id not in self.nodes, f"{node.id} already registered."

        self.nodes[node.id] = node

        # Add a update_'node' method to object
        setattr(self, "update_" + node.id,
                lambda value: self.update_node(node.id, value))

        # Add get_`node` method to object
        setattr(self, "get_" + node.id,
                lambda: self.get_node(node.id)).get_property()

        if self.nodes_published:  # update, publish property changes
            self.publish_nodes(self.retained, self.qos)

    def remove_node(self, node_id):  # not tested, needs work removing topics
        del self.nodes[node_id]

        if self.nodes_published:  # update, publish property changes
            self.publish_nodes(retain=False)

    def get_node(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id]
        else:
            return None

    def publish_nodes(self, retain=True, qos=1):
        nodes = ",".join(self.nodes.keys())
        self.publish("/".join((self.topic, "$nodes")), nodes, retain, qos)

        self.nodes_published = True

        for _, node in self.nodes.items():
            node.publish_attributes(retain, qos)

    def broadcast_handler(self, topic, payload):  # TBD
        logger.debug(
            f"Device MQTT Homie Broadcast:  Topic {topic}, Payload {payload}")

    def publish(self, topic, payload, retain, qos):
        logger.debug(
            f"Device MQTT publish topic: {topic}, retain {retain}, qos {qos}, payload: {payload}")
        self.mqtt_client.publish(topic, payload, retain=retain, qos=qos)

    def _validate_homie_settings(self, settings):
        if settings is not None:
            for setting, value in self.DEFAULT_HOMIE_SETTINGS.items():
                logger.debug("Homie settings {} {}".format(setting, value))
                if setting not in settings:
                    settings[setting] = self.DEFAULT_HOMIE_SETTINGS[setting]
        else:
            settings = self.DEFAULT_HOMIE_SETTINGS

        return settings

    def on_mqtt_connection(self, connected):
        logger.info(f"Device MQTT Connected state is {connected}")

        if connected:
            if self._mqtt_connected is False:
                self._mqtt_connected = True
                self.publish_attributes()
                self.publish_nodes()
                self.subscribe_topics()
        else:
            self._mqtt_connected = False

    def on_mqtt_message(self, topic, payload, retain, qos):
        if topic in self.mqtt_subscription_handlers:
            logger.debug(f"Device MQTT Message: Topic {topic}, "
                         + "Payload {payload} "
                         + "Retain {retain}  QOS {qos}")

            if not retain:
                # OH2.5 MQTT sends set messages with retain true - need to
                #  check to avoid this problem
                self.mqtt_subscription_handlers[topic](topic, payload)
            else:
                logger.warning(f"Device MQTT Message received with "
                               + "RETAIN TRUE: Topic {topic}, "
                               + "Payload {payload} Retain {retain}  QOS {qos}")

    @staticmethod
    def close_devices(*arg):
        logger.info('Closing Devices')
        for device in device_states.devices:
            device.close()
        logger.info('Closed Devices')

        close_mqtt_clients()
