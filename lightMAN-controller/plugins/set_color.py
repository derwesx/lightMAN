import random
import typing
import time

from classes.projector import *
from plugins.plugin import Plugin


# PLUGIN SHOULD GIVE ONLY MEANINGFUL DMX_CHANNELS DATA
# RGB parameter does not exist in LIGHT/SPOT

class SetColorPlugin(Plugin):
    time_per_cycle = 3
    R = 100
    G = 255
    B = 0
    random_color = False

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id
        self.start_time = time.perf_counter()
        self.last_time_cor = None

    def get_no_of_cycle(self):
        current_time = time.perf_counter()
        difference = current_time - self.start_time
        no_of_cycle = difference // self.time_per_cycle
        return no_of_cycle

    def proceed_data(self, projectors: typing.List[Projector]):
        if self.random_color:
            time_cor = self.get_no_of_cycle()
            if time_cor != self.last_time_cor:
                self.R_tmp = random.randint(0, 255)
                self.G_tmp = random.randint(0, 255)
                self.B_tmp = random.randint(0, 255)
                self.last_time_cor = time_cor

            for projector in projectors:
                if projector.type == "Light" or projector.type == "Spot":
                    continue
                projector.data["r"]["is_changed"] = 1
                projector.data["g"]["is_changed"] = 1
                projector.data["b"]["is_changed"] = 1
                projector.data["r"]["value"] = self.R_tmp
                projector.data["g"]["value"] = self.G_tmp
                projector.data["b"]["value"] = self.B_tmp
            for connected_node in self.connections:
                connected_node.proceed_data(projectors)
        else:
            for projector in projectors:
                if projector.type == "Light" or projector.type == "Spot":
                    continue
                projector.data["r"]["is_changed"] = 1
                projector.data["g"]["is_changed"] = 1
                projector.data["b"]["is_changed"] = 1
                projector.data["r"]["value"] = self.R
                projector.data["g"]["value"] = self.G
                projector.data["b"]["value"] = self.B
            for connected_node in self.connections:
                connected_node.proceed_data(projectors)
