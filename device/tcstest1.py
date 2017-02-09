import tcs34725
from machine import I2C, Pin, unique_id
import time
import network
#  from umqtt.simple import MQTTCLient

labNetwork = 'EEERover'
labPassword = 'exhibition'
brokerAddress = '192.168.0.10'


def connectWiFi(ssid, password):
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    if not wlan.isconnected():      # check if the station is connected to an AP
        wlan.connect(ssid, password) # connect to an AP
        while not wlan.isconnected():
            print('.', end='')
            time.sleep_ms(500)
        print('Connected!')
    wlan.config('mac')      # get the interface's MAC adddress

    print('Network config', wlan.ifconfig())

connectWiFi(labNetwork, labPassword)

#  client = MQTTCLient(machine.unique_id(), brokerAddress)
#  client.connect()
#  client.publish("Test topic", bytes('Text message', 'utf-8'))
#  i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

#  sensor = tcs34725.TCS34725(i2c)
#  sensor.gain(16)
#  
#  for _ in range(10):
#      t = time.time()
#      s = sensor.read(True)
#      t = time.time() - t
#      t += 1
#      time.sleep(0.5)
#      #print("%f" % t)
#      print(s)
#  
#sensor.active(False)


