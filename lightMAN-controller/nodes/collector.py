import typing

from projector import Projector
from plugin import Plugin


class Collector(Plugin):

    def __str__(self):
        translator_data = "Translator #" + str(self.node_id)
        return translator_data

    def __init__(self, node_id):
        self.node_id = node_id
        self.dmx_out = []
        self.connections = []

    def proceed_data(self, projectors: typing.List[Projector]):
        self.send_data(projectors)
