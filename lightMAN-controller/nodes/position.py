import typing

from projector import *
from plugin import Plugin


class PositionPlugin(Plugin):
    pan = 0
    tilt = 0

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            projector.data["pan"]["is_changed"] = 1
            projector.data["pan"]["value"] = self.pan
            projector.data["tilt"]["is_changed"] = 1
            projector.data["tilt"]["value"] = self.tilt
        self.send_data(projectors)