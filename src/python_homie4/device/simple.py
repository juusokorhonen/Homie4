#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
from .base import BaseDevice
from ..node import BaseNode
import logging

logger = logging.getLogger(__name__)


class SimpleDevice(BaseDevice):
    """A simple device with a single node.
    """

    def __init__(self, device_id=None, name=None,
                 *, node=None, **kwargs):
        """Initializes a SimpleDevice with a single node of type `node`.

        Parameters
        ----------
        device_id : str
            Device ID for MQTT topic.

        name : str
            Human readable name of device.

        node : str or BaseNode
            The single node to attach to this device.
            If `node` is a string, then a node corresponding to that type
            is searched. AttributeError is raised if node type is not found.
            Alternatively, `node` can be already a subclass of BaseNode.

        """
        super().__init__(device_id, name, **kwargs)

        # Extract node information
        if isinstance(node, BaseNode):
            self.add_node(node)
            node_id = node.id
        else:
            try:
                #node_module_name = str(node).lower()
                node_module_name = "node"
                node_id = str(node).lower()
                node_name = node_id[0].upper() + node_id[1:].lower()

                node_module = importlib.import_module("..."+node_module_name, package=__name__)   # noqa: E501

                node_class_name = node[0].upper() + node[1:] + "Node"   # noqa: E501
                Node = getattr(node_module, node_class_name)

                node_obj = Node(self, node_id, node_name, type_=node.lower())
                self.add_node(node_obj)

            except ImportError as e:
                logger.error(f"Could not import module with name "
                             + f"'{node_module_name}'. Reason: {e}.")
                raise AttributeError(f"Could not import module with name "
                                     + f"'{node_module_name}'. Reason: {e}.")

        # Add a update_'node' method to class
        setattr(self, "update_" + node_id,
                lambda value: self.update_node(node_id, value))

        # Override get_node
        setattr(self, "get_node",
                lambda: self.get_node(node_id))

        def update_node(self, name, value):
            """Updates the node with `name` with `value`.
            """
            self.get_node(name).update_value(value)
            logger.debug(f"Node '{name}' updated to '{value}'")
