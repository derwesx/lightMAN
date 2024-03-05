from projector import *


class Scene:
    projectors = []
    dmx_data = [0, ] * 512

    def __str__(self):
        scene_data = "Scene #" + str(self.node_id)
        return scene_data

    def __init__(self, node_id):
        self.node_id = node_id

    def load(self):
        import sqlite3
        conn = sqlite3.connect('./db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM \'projectors_info\'')
        projectors_fetched = cursor.fetchall()
        for projector in projectors_fetched:
            projector_id, projector_type, dmx_start = projector[0], projector[1], projector[3]
            if projector_type == 'led':
                self.projectors.append(Led(projector_id, dmx_start))
            elif projector_type == 'light':
                self.projectors.append(Light(projector_id, dmx_start))
            elif projector_type == 'wash' or projector_type == 'washS':
                self.projectors.append(Wash(projector_id, dmx_start))
            elif projector_type == 'spot':
                self.projectors.append(Spot(projector_id, dmx_start))

    def add(self, projector):
        self.projectors.append(projector)
        # Frontend addition

    def remove(self, projector_id: int):
        for projector in self.projectors:
            if projector.id == projector_id:
                del projector
                break
        # Frontend deletion

    def proceed_data(self, dmx_in):
        for dmx_channel, dmx_value in dmx_in:
            self.dmx_data[dmx_channel] = dmx_value

    def get_data(self):
        # Colors + Brightness + ... to the frontend
        return self.dmx_data

    def end_cycle(self):
        self.dmx_data = [0, ] * 512
