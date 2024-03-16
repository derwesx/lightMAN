import logging
import time
import copy

from abc import ABC, abstractmethod


class Plugin(ABC):
    time_per_cycle = 3
    start_time = 0
    node_id = "Unknown"

    def __str__(self):
        plugin_data = type(self).__name__ + " #" + str(self.node_id)
        return plugin_data

    def get_coefficient_from_time(self):
        try:
            current_time = time.perf_counter()
            difference = current_time - self.start_time
            since_cycle = difference - difference // self.time_per_cycle * self.time_per_cycle
            return since_cycle / self.time_per_cycle
        except ZeroDivisionError as error:
            logging.info(f"Trying to divide by zero in 'get coefficient' {type(self).__name__}: " + self.node_id)

    def send_data(self, projectors, node_id=None):
        deep_copy_projectors = copy.deepcopy(projectors)
        for connected_node in self.connections:
            if connected_node is not None:
                if node_id:
                    if connected_node.node_id == node_id:
                        connected_node.proceed_data(deep_copy_projectors)
                else:
                    connected_node.proceed_data(deep_copy_projectors)
