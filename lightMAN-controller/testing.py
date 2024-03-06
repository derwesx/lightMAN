from controller import Controller
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

a = Controller()

scene = a.create_node("scene")
environment = a.create_node("environment")
for i in range(0, 50):
    environment.add(i)


plugin = a.create_node("blink")
turn_on = a.create_node("turn_on")
color_plugin = a.create_node("set_color")
translator = a.create_node("translator")

# First environment -> Plugin -> Color_Plugin -> Translator
a.connect_nodes(environment.node_id, turn_on.node_id)
a.connect_nodes(turn_on.node_id, color_plugin.node_id)
a.connect_nodes(color_plugin.node_id, translator.node_id)

# Translator -> Scene
a.connect_nodes(translator.node_id, scene.node_id)

a.start()
