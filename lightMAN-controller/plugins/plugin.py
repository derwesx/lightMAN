from abc import ABC, abstractmethod


class Plugin(ABC):
    connections = []

    def __str__(self):
        plugin_data = type(self).__name__ + " #" + str(self.node_id)
        return plugin_data
