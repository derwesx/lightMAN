import logging
import typing
import time

from .projector import *
from .plugin import Plugin


class RampUpPlugin(Plugin):
    brightness = 255

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id

    def proceed_data(self, projectors: typing.List[Projector]):
        time_cor = self.get_coefficient_from_time()
        for projector in projectors:
            projector.data["dim"]["is_changed"] = 1
            projector.data["dim"]["value"] = int(time_cor * 255)
        self.send_data(projectors)
