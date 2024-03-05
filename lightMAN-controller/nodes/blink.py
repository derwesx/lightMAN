import typing
import time

from projector import *
from plugin import Plugin


class BlinkPlugin(Plugin):
    time_per_cycle = 2
    brightness = 255
    count_of_groups = 4  # ONLY WITH turn_one = False,
    # count_of_groups = From 1 to infinity, amount of groups projectors being divided into
    turn_one = False

    def __init__(self, node_id):
        self.connections = []
        self.node_id = node_id
        self.start_time = time.perf_counter()

    def get_coefficient_from_time(self):
        current_time = time.perf_counter()
        difference = current_time - self.start_time
        since_cycle = difference - difference // self.time_per_cycle * self.time_per_cycle
        return since_cycle / self.time_per_cycle

    def calculate_brightness(self, number_of_projector):
        dim_data = []

        time_cor = self.get_coefficient_from_time()
        if self.turn_one:
            time_per_one = self.time_per_cycle / number_of_projector
            current_projector = int(self.time_per_cycle * time_cor / time_per_one)
            dim_data.append([current_projector, 255])
        else:
            count_per_group = number_of_projector // self.count_of_groups
            time_per_group = self.time_per_cycle / self.count_of_groups
            current_group = int(self.time_per_cycle * time_cor / time_per_group)
            phase = number_of_projector // count_per_group
            for projector_id in range(current_group, number_of_projector, phase):
                dim_data.append([projector_id, 255])
        return dim_data

    def proceed_data(self, projectors: typing.List[Projector]):
        dim_data = self.calculate_brightness(len(projectors))
        for projector_id, dmx_value in dim_data:
            projectors[projector_id].data["dim"]["is_changed"] = 1
            projectors[projector_id].data["dim"]["value"] = dmx_value
        for connected_node in self.connections:
            connected_node.proceed_data(projectors)
