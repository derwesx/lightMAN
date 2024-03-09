import logging
import random
import typing
import time

from projector import *
from plugin import Plugin


# PLUGIN SHOULD GIVE ONLY MEANINGFUL DMX_CHANNELS DATA
# RGB parameter does not exist in LIGHT/SPOT

class SetColorPlugin(Plugin):
    R = 255
    G = 255
    B = 255

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            projector.data["r"]["is_changed"] = 1
            projector.data["g"]["is_changed"] = 1
            projector.data["b"]["is_changed"] = 1
            projector.data["r"]["value"] = self.R
            projector.data["g"]["value"] = self.G
            projector.data["b"]["value"] = self.B
        self.send_data(projectors)
