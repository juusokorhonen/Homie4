#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta
import asyncio
from ..helpers import validate_id
from .property import BaseProperty


class BaseNode(metaclass=ABCMeta):
    def __init__(self, id, name, type_, retain=True, qos=1):
        assert validate_id(id), "Node ID {} is not valid".format(id)

        self.id = id
        self.name = name
        self.type = type_
        self._device = None

        self.retain = retain
        self.qos = qos

        self.properties = {}

        self.topic = self.device.topic

        self.published = False

    @property
    def device(self):
        """Returns the device this node is bound to.

        """
        return self._device

    @device.setter
    def device(self, device):
        """Sets the `device` this node is bound to.
        """
        assert self.device is None, "Device is already set."
        self._device = device

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, parent_topic):
        self._topic = "/".join([parent_topic, self.id])

    def add_property(self, _property: BaseProperty):
        """Adds a new property to this node.

        Parameters
        ----------
        _property : BaseProperty
            The property to register to this node.
        """
        assert _property.id not in self.properties, "Property already added"

        self.properties[_property.id] = _property
        if self.published:  # need to update publish property changes
            self.publish_properties()

    def remove_property(self, property_id: str):
        """Removes (unregisters) a property from this node.

        Parameters
        ----------
        property_id : str
            The id of the property to remove.
        """
        _property = self.properties[property_id]
        del self.properties[property_id]

        # TODO: This code should be handled as a callback in the parent device
        if self.device:
            if self.device.start_time is not None:  # running, publish property changes
                self.publish_properties()
                _property.publish_attributes(False, 1)

    def get_property(self, property_id: str):
        """Returns the property identified by `property_id`.

        Parameters
        ----------
        property_id : str
            Identifier of the property to return

        Returns
        -------
        property : BaseProperty
            if `property_id` is valid
        None,
            otherwise

        """
        return self.properties.get(property_id)

    def set_property_value(self, property_id: str, value):
        """Sets the value of the property identified by `property_id` to `value`.

        Parameters
        ----------
        property_id : str
            Identifier of the property to modify.
        value
            New value for the property.
        Raises
        ------
        KeyError
            if `property_id` is invalid.

        """
        try:
            self.get_property(property_id).value = value
        except AttributeError:
            raise KeyError(
                f"Property id `{property_id}` not found in properties.")

    def publish(self, topic, payload, retain, qos):
        """Publishes a message to mqtt.

        Parameters
        ----------
        topic : str
        payload : str
        retain : str
        qos : int

        Notes
        -----
        This functionality belongs to the device instead of the node.

        """
        # TODO: Implement this with a callback in device
        if self.device:
            self.device.publish(topic, payload, retain, qos)

    def property_publisher(self, topic, payload, retain, qos):
        """Publishes a property to mqtt.

        Parameters
        ----------
        topic : str
        payload : str
        retain : str
        qos : int

        Notes
        -----
        This functionality belongs to the device instead of the node.

        """
        # TODO: Implement this with a callback in device
        if self.published:  # only publish if the node has been published
            if self.device:
                self.device.publish(topic, payload, retain, qos)

    def publish_attributes(self, retain=True, qos=1):
        """Publishes the attributes of this node.

        Parameters
        ----------
        retain : str
        qos : int

        Notes
        -----
        This functionality belongs to the device instead of the node.

        """
        # TODO: Implement this with a callback in device
        self.publish("/".join((self.topic, "$name")), self.name, retain, qos)
        self.publish("/".join((self.topic, "$type")), self.type, retain, qos)

        self.publish_properties()

    def publish_properties(self, retain=True, qos=1):
        """Publishes the attributes of this node.

        Parameters
        ----------
        retain : str
        qos : int

        Notes
        -----
        This functionality belongs to the device instead of the node.

        """
        # TODO: Implement this with a callback in device
        properties = ",".join(self.properties.keys())
        self.publish("/".join((self.topic, "$properties")),
                     properties, retain, qos)

        self.published = True  # node basics published

        for _, _property in self.properties.items():
            # print ('NODE PUBLISH PROP ',_property.name)
            _property.publish_attributes(retain, qos)

    def get_subscriptions(self):
        subscriptions = {}

        for _, _property in self.properties.items():
            subscriptions.update(_property.get_subscriptions())

        return subscriptions
