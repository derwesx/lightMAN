import typing

from projector import Projector


class Translator:

    def __str__(self):
        translator_data = "Translator #" + str(self.node_id)
        return translator_data

    def __init__(self, node_id):
        self.node_id = node_id
        self.dmx_out = []
        self.connections = []

    def proceed_data(self, projectors: typing.List[Projector]):
        for projector in projectors:
            for key in projector.data:
                key_data = projector.data[key]
                dmx_channel = key_data["dmx_channel"]
                is_changed = key_data["is_changed"]
                value = key_data["value"]
                if is_changed is False:
                    continue
                self.dmx_out.append([dmx_channel, value])
        for connected_node in self.connections:
            connected_node.proceed_data(self.dmx_out)
        self.dmx_out = []
