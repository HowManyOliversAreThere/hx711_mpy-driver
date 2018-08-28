from machine import freq
import time
from hx711 import HX711

freq(160000000)

my_hx711 = HX711()
print("HX711 offset: %.1f" % my_hx711.offset)

count = 0
while True:
    time.sleep(3)
    count += 1
    print("HX711 value %i: %.1f" % (count, my_hx711.read()))
