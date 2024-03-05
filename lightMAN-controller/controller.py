from threading import Thread
import importlib
import time
import uuid

import sacn


from nodes import *
# <<<--- CREATED NODES --->>>
NODE_NAME = dict()
NODE_NAME["turn_on"] = "TurnOnPlugin"
NODE_NAME["ramp_up"] = "RampUpPlugin"
NODE_NAME["blink"] = "BlinkPlugin"
NODE_NAME["set_color"] = "SetColorPlugin"
NODE_NAME["environment"] = "Environment"
NODE_NAME["scene"] = "Scene"
NODE_NAME["translator"] = "Translator"


# <<<--- END OF CREATED PLUGINS --->>>

def get_new_id():
    return str(uuid.uuid4())


class Controller:
    nodes = []
    environments = []
    scenes = []
    current_scene_id = None
    updates_counter = 0

    def __init__(self):
        self.sender = sacn.sACNsender(fps=60)
        self.sender.start()
        self.sender.activate_output(1)
        self.sender[1].multicast = True
        self.update_thread = Thread(target=self.update)

    def start(self):
        self.update_thread.run()

    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def create_node(self, node_type: str):
        plugin = importlib.import_module(node_type)
        try:
            class_ = getattr(plugin, NODE_NAME[node_type])
        except Exception as error:
            raise Exception("Node: " + str(NODE_NAME[node_type]) + " not found.")
        plugin_instance = class_(get_new_id())
        self.nodes.append(plugin_instance)
        if type == "environment":
            self.environments.append(plugin_instance)
        if type == "scene" and self.current_scene_id is None:
            self.current_scene_id = plugin_instance.node_id
        return plugin_instance

    def delete_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                self.nodes.remove(node)
        if node in self.environments:
            self.environments.remove(node)
        if node in self.scenes:
            self.scenes.remove(node)
        if len(self.scenes) == 0:
            self.current_scene_id = None

    def connect_nodes(self, from_id, to_id):
        from_node = None
        to_node = None
        for node in self.nodes:
            if node.node_id == from_id:
                from_node = node
            if node.node_id == to_id:
                to_node = node
        if from_node is None or to_node is None:
            raise Exception("Node not found")
        if to_node in from_node.connections:
            ...
            # Nodes are already connected
        else:
            from_node.connections.append(to_node)

    def disconnect_nodes(self, from_id, to_id):
        from_node = None
        to_node = None
        for node in self.nodes:
            if node.node_id == from_id:
                from_node = node
            if node.node_id == to_id:
                to_node = node
        if from_node is None or to_node is None:
            raise Exception("Node not found")
        from_node.connections.remove(to_node)

    def update(self):
        while True:
            self.updates_counter += 1
            for environment in self.environments:
                environment.proceed_data()
            for scene in self.scenes:
                if scene.node_id == self.current_scene_id:
                    self.sender[1].dmx_data = scene.get_data()[1:] + [0]
                # UPDATE FRONTEND
                scene.end_cycle()
            for environment in self.environments:
                environment.end_cycle()
