import typing

from projector import *
from plugin import Plugin


class Shutter(Plugin):
    shutter = 0
    color = 0 # TEMP SOLUTION

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            projector.data["shutter"]["is_changed"] = 1
            projector.data["shutter"]["value"] = self.shutter
            projector.data["color"]["is_changed"] = 1
            projector.data["color"]["value"] = self.color
        self.send_data(projectors)
