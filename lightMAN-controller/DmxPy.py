import sys, time
import threading
import pyftdi.serialext


class DmxPy:
    def __init__(self, serialPort):
        try:
            self.serial = pyftdi.serialext.serial_for_url(serialPort, baudrate=250000, stopbits=2)
        except Exception as e:
            print(e)
            print("Error: could not open Serial Port")
            sys.exit(0)
        self.dmxData = [bytes([0])] * 513
        self.dmxData[0] = bytes([0])

    def setChannel(self, chan, intensity):
        if chan > 512: chan = 512
        if chan < 0: chan = 0
        if intensity > 255: intensity = 255
        if intensity < 0: intensity = 0
        self.dmxData[chan] = bytes([intensity])

    def setFull(self, dmxData):
        for i in range(len(dmxData)):
            self.dmxData[i] = bytes([dmxData[i]])

    def blackout(self):
        for i in range(1, 512, 1):
            self.dmxData[i] = bytes([0])

    def render(self):
        sdata = b''.join(self.dmxData)
        self.serial.write(sdata)

    def display_universe(self):
        while True:
            self.render()
            time.sleep(0.005)
