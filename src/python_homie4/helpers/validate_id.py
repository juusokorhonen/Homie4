#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def validate_topic(id):
    """Validate a topic ID according to the homie defintion
    https://homieiot.github.io/specification/#topic-ids

    Parameters
    ----------
    id : str
        Topic id string to validate.

    Returns
    -------
    True, if valid topic id
    False, otherwise

    Notes
    -----
    An MQTT topic consists of one or more topic levels, separated by the slash
    character (/). A topic level ID MAY contain lowercase letters from a to z,
    numbers from 0 to 9 as well as the hyphen character (-).
    A topic level ID MUST NOT start or end with a hyphen (-). The special
    character $ is used and reserved for Homie attributes. The underscore (_)
    is used and reserved for Homie node arrays.

    """
    assert isinstance(id, str)
    r = re.compile("(^(?!\\-)[a-z0-9\\-]+(?<!\\-)$)")
    return id if r.match(id) else False
