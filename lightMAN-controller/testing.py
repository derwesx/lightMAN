from controller import Controller

a = Controller()

scene = a.create_scene()
scene.load()
environment = a.create_environment()
environment2 = a.create_environment()
for i in range(0, 35):
    environment.add(i)

for i in range(35, 50):
    environment2.add(i)

plugin = a.create_plugin("blink")
turn_on = a.create_plugin("turn_on")
color_plugin = a.create_plugin("set_color")
color_plugin2 = a.create_plugin("set_color")
translator = a.create_translator()

# First environment -> Plugin -> Color_Plugin -> Translator
a.connect_nodes(environment.node_id, plugin.node_id)
a.connect_nodes(plugin.node_id, color_plugin.node_id)
a.connect_nodes(color_plugin.node_id, translator.node_id)

# Second environment -> Color_Plugin -> Translator
a.connect_nodes(environment2.node_id, color_plugin2.node_id)
a.connect_nodes(color_plugin2.node_id, turn_on.node_id)
a.connect_nodes(turn_on.node_id, translator.node_id)

# Translator -> Scene
# a.connect_nodes(translator.node_id, scene.node_id)

a.start()
