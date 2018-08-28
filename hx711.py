import time
from machine import Pin

# We use a separate toggle function and the @micropython.native
# decorator in order to get a pin toggle quick enough to make
# the readings from the hx711 sensor valid
@micropython.native
def toggle(p):
    #now = time.ticks_us()
    p.value(1)
    p.value(0)
    #then = time.ticks_us()
    #print(time.ticks_diff(then, now))

class HX711:
    def __init__(self, pd_sck=14, dout=12, gain=128):
        self.gain = gain
        if self.gain != 128: return("Error: Gain not supported")
        self.SCALING_FACTOR = 229
        self.dataPin = Pin(dout, Pin.IN)
        self.pdsckPin = Pin(pd_sck, Pin.OUT, value=0)
        self.powerUp()
        self.tare()
        self.value = 0

    # Prepares the hx711 sensor for reading
    def powerUp(self):
        self.pdsckPin.value(0)
        self.powered = True

    # Places the hx711 sensor into a low power mode, with no read capability
    def powerDown(self):
        if self.powered:
            self.pdsckPin.value(1)
            self.powered = False

    # Checks if the hx711 sensor has a reading ready
    # TODO: Add timeout and error if sensor not getting ready
    def isready(self):
        time.sleep(.001)
        return self.dataPin.value()

    # Function for getting raw value from sensor
    # Designed for internal use only - read() should be used by humans
    def raw_read(self):
        if not self.powered:
            return("Error: Cannot read, HX711 not powered")
        
        while not self.isready():
            pass
        time.sleep_us(10)
        my = 0
        for idx in range(24):
            toggle(self.pdsckPin)
            data = self.dataPin.value()
            # Data is twos complement so need to check if first bit is high
            if not idx:
                neg = data
            else:
                my = ( my << 1) | data
        toggle(self.pdsckPin)
        if neg: my = my - (1<<23)
        return round(my/self.SCALING_FACTOR, 1)
    
    # Sets the zero point of the sensor
    def tare(self):
        self.offset = self.raw_read()
        return self.offset
    
    # Returns the current weight value, in grams
    def read(self):
        self.value = round(self.raw_read() - self.offset, 1)
        return self.value
