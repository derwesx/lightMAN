import typing
import time

from projector import *
from plugin import Plugin


class SwitchPlugin(Plugin):
    time_per_switch = 3
    brightness = 255

    def __init__(self, node_id):
        self.start_time = time.perf_counter()
        self.connections = []
        self.node_id = node_id

    def get(self):
        ids = []
        for connection in self.connections:
            ids.append(connection.node_id)
        need_id = self.get_group_from_time()
        if need_id == -1:
            return -1
        else:
            return ids[need_id]

    def get_group_from_time(self):
        current_time = time.perf_counter()
        difference = current_time - self.start_time
        no_of_cycle = difference // self.time_per_switch
        if len(self.connections):
            return no_of_cycle % len(self.connections)
        else:
            return -1

    def proceed_data(self, projectors: typing.List[Projector]):
        need_id = self.get()
        for connected_node in self.connections:
            if connected_node.node_id == need_id:
                connected_node.proceed_data(projectors)
                break
