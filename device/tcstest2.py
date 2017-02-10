import tcs34725
from machine import I2C, Pin, unique_id
import time
import network
from umqtt.simple import MQTTClient
import json

#To-Do: get time data from server

#----------------------------------------I/O pins---------------------------------------------------
allowReadPin = Pin(14, Pin.IN, None)
#----------------------------------------WiFi setup-------------------------------------------------
labNetwork = 'EEERover'
labPassword = 'exhibition'
brokerAddress = '192.168.0.10'
deviceName = 'esp8266_' + str(unique_id(), 'utf-8')

def connectWiFi(ssid, password):
    wlan = network.WLAN(network.STA_IF)                 # create station interface
    wlan.active(True)                                   # activate the interface
    if not wlan.isconnected():                          # check if the station is connected to an AP
        wlan.connect(ssid, password)                    # connect to an AP
        while not wlan.isconnected():
            print('.', end = '')
            time.sleep_ms(500)
        print('Connected!')
    wlan.config('mac')                                  # get the interface's MAC adddress

    print('Network config', wlan.ifconfig())

connectWiFi(labNetwork, labPassword)
#----------------------------------------MQTT client setup------------------------------------------
def sub_cb(topic,msg):
    print(msg)

client = MQTTClient(deviceName, brokerAddress)
client.set_callback(sub_cb)
#----------------------------------------Sensor setup-----------------------------------------------
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = tcs34725.TCS34725(i2c)
sensor.gain(16)

def convert_rgb_data(raw_rgb):
    #corrected_data = (raw_rgb[0]/0.88,raw_rgb[1]/0.66, raw_rgb[2]/0.57,raw_rgb[3]/1)
    const = 255/1024
    corrected_data = raw_rgb
    corrected_data = (  int(round(corrected_data[0]*const, 0)), 
                        int(round(corrected_data[1]*const, 0)),
                        int(round(corrected_data[2]*const, 0)),
                        int(round(corrected_data[3]*const, 0)))
    return corrected_data
#----------------------------------------Data reading-----------------------------------------------
while True:
    #print(allowReadPin.value())
    if allowReadPin.value() == 1:
        client.connect()
        client.subscribe('esys/TBA/sensor')
        s = sensor.read(True)
        s = convert_rgb_data(s)
        payload = json.dumps({'RGBC Data': {'R':s[0],'G':s[1],'B':s[2],'C':s[3]},'time':'4:20'})
        #client.publish('esys/TBA/sensor', 'RGBC: ('+ str(s[0]) + ', '+ str(s[1]) + ', ' + str(s[2]) + ', ' + str(s[3]) +')')
        client.publish('esys/TBA/sensor',payload)
        time.sleep_ms(100)
        client.wait_msg()
        client.disconnect()
