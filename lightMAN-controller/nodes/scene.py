import importlib
import logging

from projector import *
from translator import Translator


class Scene:
    projectors = []
    dmx_data = [0, ] * 513

    def __str__(self):
        scene_data = "Scene #" + str(self.node_id)
        return scene_data

    def __init__(self, node_id):
        self.translator = Translator(-404)
        self.translator.connections.append(self)
        self.node_id = node_id

    def load(self):
        import sqlite3
        conn = sqlite3.connect('./db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM \'projectors_info\'')
        projectors_fetched = cursor.fetchall()
        for projector in projectors_fetched:
            projector_id, projector_type, dmx_start = projector[0], projector[1], projector[3]
            projector_type = projector_type.title()
            try:
                projector_module = importlib.import_module("projector")
                _projector_class = getattr(projector_module, projector_type)
                self.projectors.append(_projector_class(projector_id, dmx_start))
            except Exception as error:
                logging.error("Projector with model: " + projector_type + " not found.\n" + str(error))

    def add(self, projector):
        self.projectors.append(projector)
        # Frontend addition

    def remove(self, projector_id: int):
        for projector in self.projectors:
            if projector.id == projector_id:
                del projector
                break
        # Frontend deletion

    def proceed_data(self, projectors):
        self.translator.proceed_data(projectors)

    def proceed_data_dmx(self, dmx_in):
        for dmx_channel, dmx_value in dmx_in:
            self.dmx_data[dmx_channel] = dmx_value

    def get_data(self):
        # Colors + Brightness + ... to the frontend
        return self.dmx_data

    def end_cycle(self):
        self.dmx_data = [0, ] * 512
