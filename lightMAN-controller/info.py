# <<<---- GLOBAL INFO ---->>>
# 1. All classes gets their id in __init__
# 2. Method for calculation SHOULD be named as proceed_data
# 3. Page is being updated in the way:
# 3.1 Environment.proceed_data()
# 3.2 Scene.get_data()
# 3.3 Scene.end_cycle()
# 4. Every node has its unique id
# 5. PLUGIN SHOULD GIVE ONLY MEANINGFUL DMX_CHANNELS DATA
# RGB parameter does not exist in LIGHT/SPOT, etc.
# <<<---- Scene ---->>>

# dmx_in attribute: [[dmx_adress, value (0-255)], ...]
dmx_in = [[2, 255], [3, 127], [15, 0]]


# proceed_data: gets dmx_in array from translator and adds it to the current dmx_data
def proceed_data(self, dmx_in):
    for dmx_channel, dmx_value in dmx_in:
        self.dmx_data[dmx_channel] = dmx_value


# update_data: sends all dmx data to the network, then nullifies all current data
def update_data(self):
    # Colors + Brightness + ... to the frontend
    self.sender[1].dmx_data = self.dmx_data
    dmx_data = [0, ] * 512

# <<<---- Projector ---->>>
# Every parameter is stored as three dictionaries [15, 0, 0], [12, 1, 200] [dmx_channel, is_changed, value]
# All values are stored in a dict: {"color" : {"dmx_channel": ..., "is_changed": ..., "value": ...], ... }
# Projector is abstract class: Wash, Light, Spot, Led
