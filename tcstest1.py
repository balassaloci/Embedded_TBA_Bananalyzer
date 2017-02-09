import tcs34725
from machine import I2C, Pin
import time

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

sensor = tcs34725.TCS34725(i2c)
sensor.gain(60)

for _ in range(10):
    t = time.time()
    s = sensor.read(True)
    t = time.time() - t
    t += 1
    time.sleep(0.5)
    #print("%f" % t)
    print(s)

#sensor.active(False)


