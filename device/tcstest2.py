import tcs34725
from machine import I2C, Pin, unique_id
from machine import RTC
import time
import network
from umqtt.simple import MQTTClient
import json

#To-Do: get time data from server
date = 0, 0, 0, 0, 0, 0
#----------------------------------------I/O pins-------------------------------
allowReadPin = Pin(14, Pin.IN, None)    # Switch input pin14 without pull res.
#----------------------------------------WiFi setup-----------------------------
labNetwork = 'EEERover'
labPassword = 'exhibition'
brokerAddress = '192.168.0.10'
deviceName = 'esp8266_' + str(unique_id(), 'utf-8')

def connectWiFi(ssid, password):
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)                   # activate the interface
    if not wlan.isconnected():          # check if the station is connected
        wlan.connect(ssid, password)    # connect to an AP
        while not wlan.isconnected():
            print('.', end = '')
            time.sleep_ms(500)
        print('Connected!')
    wlan.config('mac')                  # get the interface's MAC adddress

    print('Network config', wlan.ifconfig())

connectWiFi(labNetwork, labPassword)    # connect to WiFi network
#----------------------------------------MQTT client setup----------------------
def parseDate(a):
    return  int(a[0:4]), int(a[5:7]),   \
            int(a[8:10]), int(a[11:13]),\
            int(a[14:16]), int(a[17:19]) 

def sub_cb(topic,msg):                  # callback for debu
    print(msg)
    if topic == b'esys/time':
        strMsg = msg.decode('utf-8')
        dateAndTime = json.loads(strMsg)  #decode JSON encoded time 
        global date
        dateString = dateAndTime["date"]
        date = parseDate(dateString)
        print(date)

client = MQTTClient(deviceName, brokerAddress)
client.set_callback(sub_cb)
#----------------------------------------Internal clock setup-------------------
rtc = RTC()

client.connect()
client.subscribe('esys/time')
client.wait_msg()        #get time form server
client.disconnect()

rtc.datetime((date[0], date[1], date[2], date[3], date[4], date[5], 0, 0))
#----------------------------------------RGB Sensor setup-----------------------
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = tcs34725.TCS34725(i2c)
sensor.gain(16)                         #gain: 1, 2, 16, 60 
#sensor.integration_time(402)           #change this for darker light conditions

def convert_rgb_data(raw_rgb):
    const = 255/1024                    #Convert 10 bit ADC data to 8 bit RGB
    raw_rgb = (  int(round(raw_rgb[0]*const, 0)), 
                 int(round(raw_rgb[1]*const, 0)),
                 int(round(raw_rgb[2]*const, 0)),
                 int(round(raw_rgb[3]*const, 0)))
    return raw_rgb
#----------------------------------------Data reading and uploading-------------
while True:
    if allowReadPin.value() == 1:           #If switch is on, read values
        s = sensor.read(True)               #Allow sensor read 
        s = convert_rgb_data(s)             #Convert obtained data
        
        client.connect()                    #Connect to MQTT server
        client.subscribe('esys/TBA/sensor') #Topic for data uploading
                                            #Convert data to JSON format
        #payload = json.dumps({'RGBC Data':
        #    {'R':s[0], 'G':s[1], 'B':s[2], 'C':s[3]}, 'time': rtc.now()})

        payload = json.dumps({'RGBC Data': 
            {'R':s[0],'G':s[1],'B':s[2],'C':s[3]},'time':'4:20'})

        client.publish('esys/TBA/sensor', payload)   #Upload sensor data and time
        time.sleep_ms(100)
        client.wait_msg()                   #Read uploaded data for debugging
        client.disconnect()                 #Disconnect from the server
