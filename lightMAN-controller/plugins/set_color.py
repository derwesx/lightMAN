import typing
import time

from classes.projector import *
from plugins.plugin import Plugin


# PLUGIN SHOULD GIVE ONLY MEANINGFUL DMX_CHANNELS DATA
# RGB parameter does not exist in LIGHT/SPOT

class SetColorPlugin(Plugin):
    R = 255
    G = 0
    B = 0

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            if projector.type == "Light" or projector.type == "Spot":
                continue
            projector.data["r"]["is_changed"] = 1
            projector.data["g"]["is_changed"] = 1
            projector.data["b"]["is_changed"] = 1
            projector.data["r"]["value"] = self.R
            projector.data["g"]["value"] = self.G
            projector.data["b"]["value"] = self.B
        for connected_node in self.connections:
            connected_node.proceed_data(projectors)
