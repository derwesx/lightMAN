import logging

from scene import Scene


# All purposes of the environment is to track projectors
# x-axis and y-axis and send all that data to the plugins/translators.
class Environment:

    def __str__(self):
        environment_data = "Environment #" + str(self.node_id)
        return environment_data

    def __init__(self, node_id):
        self.node_id = node_id
        self.projectors = []
        self.connections = []
        self.__scene = Scene(-1)
        self.__scene.load()

    def add(self, projector_id: int):
        projector_id = int(projector_id)
        for projector in self.__scene.projectors:
            if int(projector.id) == int(projector_id):
                self.projectors.append(projector)
                break

    def delete(self, projector_id: int):
        projector_id = int(projector_id)
        for projector in self.projectors:
            if int(projector.id) == int(projector_id):
                projector.in_use = False
                self.projectors.remove(projector)
                break

    def proceed_data(self):
        for connected_node in self.connections:
            connected_node.proceed_data(self.projectors)

    def end_cycle(self):
        for projector in self.projectors:
            for key in projector.data:
                projector.data[key]["is_changed"] = 1
                projector.data[key]["value"] = 0
