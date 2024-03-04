import time
from threading import Thread
import sacn
import uuid
import importlib

from classes.environment import Environment
from classes.translator import Translator
from classes.scene import Scene
from plugins import *

# <<<--- CREATED PLUGINS --->>>
PLUGIN_NAME = dict()
PLUGIN_NAME["turn_on"] = "TurnOn"
PLUGIN_NAME["ramp_up"] = "RampUp"
PLUGIN_NAME["blink"] = "Blink"
PLUGIN_NAME["set_color"] = "SetColor"


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

    def create_plugin(self, type: str):
        plugin = importlib.import_module(type)
        try:
            class_ = getattr(plugin, PLUGIN_NAME[type] + "Plugin")
        except Exception as error:
            raise Exception("All plugins classes should be named as {plugin_name}Plugin")
        plugin_instance = class_(get_new_id())
        self.nodes.append(plugin_instance)
        return plugin_instance

    def create_environment(self):
        new_environment = Environment(get_new_id())
        self.environments.append(new_environment)
        self.nodes.append(new_environment)
        return new_environment

    def create_scene(self):
        new_scene = Scene(get_new_id())
        self.scenes.append(new_scene)
        self.nodes.append(new_scene)
        if self.current_scene_id is None:
            self.current_scene_id = new_scene.node_id
        return new_scene

    def create_translator(self):
        new_translator = Translator(get_new_id())
        self.nodes.append(new_translator)
        return new_translator

    def delete_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                self.nodes.remove(node)
        for node in self.environments:
            if node.id == node_id:
                self.environments.remove(node)
        for node in self.scenes:
            if node.id == node_id:
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
