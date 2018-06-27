from machine import freq
import time
from hx711 import HX711

freq(160000000)

offset = HX711().value
print("offset: ", offset)

while True:
    v = HX711().value
    if (v == 0): print("Invalid")
    else:
        v -= offset
        if(v>0): print(v)
        else: print("-%s" % str(v>>1))
    time.sleep(1)
