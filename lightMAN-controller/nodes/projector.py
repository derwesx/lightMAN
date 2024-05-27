from abc import ABC, abstractmethod
from collections import OrderedDict

# <<<< AVAILABLE PARAMETERS >>>>
available_params = ["dim", "color", "r", "g", "b", "pan", "tilt", "pan_speed", "tilt_speed", "focus", "zoom", "shutter"]


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
        for parameter in available_params:
            self.data[parameter] = {}
            self.data[parameter]["dmx_channel"] = 0
            self.data[parameter]["is_changed"] = 0
            self.data[parameter]["value"] = 0
        self.calculate_channels(dmx_start)

    @abstractmethod
    def calculate_channels(self, dmx_start):
        ...  # Calculate channels according to the type


class Washh(Projector):
    keys = ["dim", "zoom", "shutter", "pan", "tilt", "r", "g", "b"]

    def calculate_channels(self, dmx_start):
        self.data["pan"]["dmx_channel"] = dmx_start  # 1
        self.data["tilt"]["dmx_channel"] = dmx_start + 2  # 3
        self.data["dim"]["dmx_channel"] = dmx_start + 5  # Dimmer
        self.data["shutter"]["dmx_channel"] = dmx_start + 6  # SHUTTER
        self.data["r"]["dmx_channel"] = dmx_start + 7  # projector id = 1
        self.data["g"]["dmx_channel"] = dmx_start + 8  # dmx_start = 4
        self.data["b"]["dmx_channel"] = dmx_start + 9  # rgb 8 9 10
        self.data["zoom"]["dmx_channel"] = dmx_start + 11  # ZOOM


class Spott(Projector):
    keys = ["dim", "zoom", "focus", "color", "shutter", "pan", "tilt"]

    def calculate_channels(self, dmx_start):
        self.data["pan"]["dmx_channel"] = dmx_start
        self.data["tilt"]["dmx_channel"] = dmx_start + 2
        self.data["dim"]["dmx_channel"] = dmx_start + 5
        self.data["shutter"]["dmx_channel"] = dmx_start + 6
        self.data["color"]["dmx_channel"] = dmx_start + 7
        self.data["focus"]["dmx_channel"] = dmx_start + 11
        self.data["zoom"]["dmx_channel"] = dmx_start + 14


class Rgb(Projector):
    keys = ["r", "g", "b"]

    def calculate_channels(self, dmx_start):
        self.data["r"]["dmx_channel"] = dmx_start
        self.data["g"]["dmx_channel"] = dmx_start + 1
        self.data["b"]["dmx_channel"] = dmx_start + 2


class Wash(Projector):
    keys = ["dim", "zoom", "shutter", "pan", "tilt", "r", "g", "b"]

    def calculate_channels(self, dmx_start):
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["shutter"]["dmx_channel"] = dmx_start + 1
        self.data["zoom"]["dmx_channel"] = dmx_start + 2
        self.data["pan"]["dmx_channel"] = dmx_start - 6
        self.data["tilt"]["dmx_channel"] = dmx_start - 5
        self.data["r"]["dmx_channel"] = dmx_start - 4
        self.data["g"]["dmx_channel"] = dmx_start - 3
        self.data["b"]["dmx_channel"] = dmx_start - 2


class Washs(Wash):
    keys = ["dim", "shutter", "r", "g", "b"]

    def calculate_channels(self, dmx_start):
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["r"]["dmx_channel"] = dmx_start + 1
        self.data["g"]["dmx_channel"] = dmx_start + 2
        self.data["b"]["dmx_channel"] = dmx_start + 3
        self.data["shutter"]["dmx_channel"] = dmx_start + 5


class Washl(Wash):
    ...


class Light(Projector):
    keys = ["dim"]

    def calculate_channels(self, dmx_start):
        self.data["dim"] = {}
        self.data["dim"]["dmx_channel"] = dmx_start


class Led(Projector):
    keys = ["dim", "r", "g", "b"]

    def calculate_channels(self, dmx_start):
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["r"]["dmx_channel"] = dmx_start - 3
        self.data["g"]["dmx_channel"] = dmx_start - 2
        self.data["b"]["dmx_channel"] = dmx_start - 1


class Spot(Projector):
    keys = ["dim", "zoom", "focus", "color", "shutter", "pan", "tilt", "pan_speed", "tilt_speed"]

    def calculate_channels(self, dmx_start):
        self.data["dim"]["dmx_channel"] = dmx_start
        self.data["zoom"]["dmx_channel"] = dmx_start + 8
        self.data["focus"]["dmx_channel"] = dmx_start + 7
        self.data["color"]["dmx_channel"] = dmx_start + 2
        self.data["shutter"]["dmx_channel"] = dmx_start + 1
        self.data["pan"]["dmx_channel"] = dmx_start - 5
        self.data["tilt"]["dmx_channel"] = dmx_start - 4
        self.data["pan_speed"]["dmx_channel"] = dmx_start - 3
        self.data["tilt_speed"]["dmx_channel"] = dmx_start - 2
