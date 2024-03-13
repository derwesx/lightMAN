import copy

from abc import ABC, abstractmethod


class Plugin(ABC):

    def __str__(self):
        plugin_data = type(self).__name__ + " #" + str(self.node_id)
        return plugin_data

    def send_data(self, projectors, node_id = None):
        deep_copy_projectors = copy.deepcopy(projectors)
        for connected_node in self.connections:
            if connected_node is not None:
                if node_id:
                    if connected_node.node_id == node_id:
                        connected_node.proceed_data(deep_copy_projectors)
                else:
                    connected_node.proceed_data(deep_copy_projectors)