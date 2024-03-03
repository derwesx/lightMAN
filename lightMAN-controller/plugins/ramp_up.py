import typing
import time

from classes.projector import *
from plugins.plugin import Plugin


class RampUpPlugin(Plugin):
    time_per_cycle = 4
    brightness = 255

    def __init__(self, node_id):
        self.node_id = node_id
        self.start_time = time.perf_counter()

    def get_coefficient_from_time(self):
        current_time = time.perf_counter()
        difference = current_time - self.start_time
        since_cycle = difference - difference // self.time_per_cycle * self.time_per_cycle
        return since_cycle / self.time_per_cycle

    def proceed_data(self, projectors: typing.List[Projector]):
        time_cor = self.get_coefficient_from_time()
        for projector in projectors:
            projector.data["dim"]["is_changed"] = 1
            projector.data["dim"]["value"] = int(time_cor * 255)
        for connected_node in self.connections:
            connected_node.proceed_data(projectors)
