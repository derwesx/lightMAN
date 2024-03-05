from abc import ABC, abstractmethod
from collections import OrderedDict


class Projector:
    in_use = False
    x_axis = 0
    y_axis = 0

    def __str__(self):
        projector_data = self.type + " #" + str(self.id) + ":\n"
        for key in self.data:
            projector_data += key + "=" + str(self.data[key]) + "\n"
        return projector_data

    def __init__(self, projector_id, dmx_start):
        self.type = type(self).__name__
        self.id = projector_id
        self.data = OrderedDict()
        self.calculate_channels(dmx_start)
        for key in self.data:
            self.data[key]["is_changed"] = 0
            self.data[key]["value"] = 0

    @abstractmethod
    def calculate_channels(self, dmx_start):
        ...  # Calculate channels according to the type


class Wash(Projector):
    def calculate_channels(self, dmx_start):
        keys = ["dim", "zoom", "shutter", "pan", "tilt", "r", "g", "b"]
        for key in keys:
            self.data[key] = {}
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["zoom"]["dmx_channel"] = dmx_start + 2
        self.data["shutter"]["dmx_channel"] = dmx_start + 1
        self.data["pan"]["dmx_channel"] = dmx_start - 6
        self.data["tilt"]["dmx_channel"] = dmx_start - 5
        self.data["r"]["dmx_channel"] = dmx_start - 4
        self.data["g"]["dmx_channel"] = dmx_start - 3
        self.data["b"]["dmx_channel"] = dmx_start - 2


class Light(Projector):
    def calculate_channels(self, dmx_start):
        self.data["dim"] = {}
        self.data["dim"]["dmx_channel"] = dmx_start


class Led(Projector):
    def calculate_channels(self, dmx_start):
        keys = ["dim", "r", "g", "b"]
        for key in keys:
            self.data[key] = {}
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["r"]["dmx_channel"] = dmx_start - 3
        self.data["g"]["dmx_channel"] = dmx_start - 2
        self.data["b"]["dmx_channel"] = dmx_start - 1


class Spot(Projector):
    def calculate_channels(self, dmx_start):
        keys = ["dim", "zoom", "focus", "color", "shutter", "pan", "tilt", "pan_speed", "tilt_speed"]
        for key in keys:
            self.data[key] = {}
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["zoom"]["dmx_channel"] = dmx_start + 8
        self.data["focus"]["dmx_channel"] = dmx_start + 7
        self.data["color"]["dmx_channel"] = dmx_start + 2
        self.data["shutter"]["dmx_channel"] = dmx_start + 1
        self.data["pan"]["dmx_channel"] = dmx_start - 5
        self.data["tilt"]["dmx_channel"] = dmx_start - 4
        self.data["pan_speed"]["dmx_channel"] = dmx_start - 3
        self.data["tilt_speed"]["dmx_channel"] = dmx_start - 2
