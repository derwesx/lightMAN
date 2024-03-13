import typing

from projector import Projector
from plugin import Plugin


class Collector(Plugin):

    def __init__(self, node_id):
        self.node_id = node_id
        self.dmx_out = []
        self.connections = []

    def proceed_data(self, projectors: typing.List[Projector]):
        self.send_data(projectors)
