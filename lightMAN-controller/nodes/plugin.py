import copy

from abc import ABC, abstractmethod


class Plugin(ABC):

    def __str__(self):
        plugin_data = type(self).__name__ + " #" + str(self.node_id)
        return plugin_data

    def send_data(self, projectors):
        deep_copy_projectors = copy.deepcopy(projectors)
        for connected_node in self.connections:
            if connected_node is not None:
                connected_node.proceed_data(deep_copy_projectors)
