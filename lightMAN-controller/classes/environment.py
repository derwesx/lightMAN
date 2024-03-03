from classes.scene import Scene
from classes.projector import Projector


# All purposes of the environment is to track projectors
# x-axis and y-axis and send all that data to the plugins/translators.
class Environment:
    projectors = []

    def __str__(self):
        environment_data = "Environment #" + str(self.node_id)
        return environment_data

    def __init__(self, node_id):
        self.node_id = node_id
        self.connections = []
        self.__scene = Scene(-1)
        self.__scene.load()

    def add(self, projector_id: int):
        for projector in self.__scene.projectors:
            if projector.id == projector_id:
                self.projectors.append(projector)

    def delete(self, projector_id: int):
        for projector in self.projectors:
            if projector.id == projector_id:
                projector.in_use = False
                del projector
                break

    def proceed_data(self):
        for connected_node in self.connections:
            connected_node.proceed_data(self.projectors)
