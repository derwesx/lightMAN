import typing

from .projector import *
from .plugin import Plugin


class TurnOnPlugin(Plugin):
    brightness = 0

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            projector.data["dim"]["is_changed"] = 1
            projector.data["dim"]["value"] = self.brightness
        for connected_node in self.connections:
            connected_node.proceed_data(projectors)
