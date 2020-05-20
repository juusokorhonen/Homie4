#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseNode
from .property import ContactProperty


class ContactNode(BaseNode):
    def __init__(
        self, device, id="contact", name="Contact", type_="contact", retain=True, qos=1
    ):
        super().__init__(device, id, name, type_, retain, qos)

        self.add_property(ContactProperty(self, "contact"))

    def update_contact(self, contact):
        self.get_property("contact").value = contact
