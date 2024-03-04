from controller import Controller

a = Controller()

scene = a.create_scene()
scene.load()
environment = a.create_environment()
environment2 = a.create_environment()
environment.add(0)
environment.add(1)
environment.add(2)

environment2.add(3)
environment2.add(4)
environment2.add(5)
plugin = a.create_plugin("blink")
color_plugin = a.create_plugin("set_color")

translator = a.create_translator()

# First environment -> Plugin -> Color_Plugin -> Translator
a.connect_nodes(environment.node_id, plugin.node_id)
a.connect_nodes(plugin.node_id, color_plugin.node_id)
a.connect_nodes(color_plugin.node_id, translator.node_id)

# Second environment -> Color_Plugin -> Translator
a.connect_nodes(environment2.node_id, color_plugin.node_id)
a.connect_nodes(color_plugin.node_id, translator.node_id)

# Translator -> Scene
a.connect_nodes(translator.node_id, scene.node_id)

a.start()
