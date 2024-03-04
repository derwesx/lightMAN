import typing

from classes.projector import *
from plugins.plugin import Plugin


class TurnOnPlugin(Plugin):
    brightness = 255

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            projector.data["dim"]["is_changed"] = 1
            projector.data["dim"]["value"] = self.brightness
        for connected_node in self.connections:
            connected_node.proceed_data(projectors)
