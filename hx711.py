import utime
import machine # import Pin
from machine import Pin
import time

class HX711:
    def __init__(self, pd_sck=14, dout=12, gain=128):
        self.gain = gain
        self.dataPin = Pin(dout, Pin.IN)
        self.pdsckPin = Pin(pd_sck, Pin.OUT, value=0)
        self.powerDown()
        self.powerUp()
        self.value = self.read()

    def isready(self):
        time.sleep(.001)
        return self.dataPin.value() == 0

    def read(self):
        self.powerUp()
        while not self.isready():
            pass
        print("<waiting finished> dataPin: {}, sckPin: {}".format(self.dataPin.value(), self.pdsckPin.value()))
        my = 0
        now = utime.ticks_us()
        myus = "0"
        mydata = ""
        for i in range(24):
            now = utime.ticks_us()
            self.pdsckPin.value(1)
            self.pdsckPin.value(0)
            myus += ", " + str(utime.ticks_diff(utime.ticks_us(), now))
            data = self.dataPin.value()
            mydata += str(data)
            my = ( my << 1) | data
        #print("bitbanged: ", my)
        #print("us: ", myus)
        #print("data: ", mydata)
        return my

        for i in range(3):
            self.pdsckPin.value(1)
            utime.sleep_us(2)
            self.pdsckPin.value(0)
            self.powerDown()

    def powerDown(self):
        self.pdsckPin.value(0)
        self.pdsckPin.value(1)
        utime.sleep_us(80)

    def powerUp(self):
        self.pdsckPin.value(0)
