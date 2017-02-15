import tcs34725
import rgb2hsl
import json
import time
from machine import I2C, Pin, unique_id, RTC
from umqtt.simple import MQTTClient

date = 0, 0, 0, 0, 0, 0, 0, 0           # set global variable
payload =""
#----------------------------------------I/O pins-------------------------------
allowReadPin = Pin(14, Pin.IN, None)    # Switch input pin14 without pull res.
#----------------------------------------Time parser----------------------------
def parseDate(a):
    return  int(a[0:4]), int(a[5:7]),   \
            int(a[8:10]), int(a[11:13]),\
            int(a[14:16]), int(a[17:19]), 0, 0 
#----------------------------------------Data uploading-------------------------
def uploadData():
    with open('JSONData.txt', 'r') as savedData:
        JSONData = savedData.read()
        client.publish('esys/TBA/sensor/data', JSONData)
    with open('JSONData.txt', 'w') as savedData:
        pass
#----------------------------------------MQTT client setup----------------------
deviceName = 'esp8266_' + str(unique_id(), 'utf-8')
brokerAddress = '192.168.0.10'

def sub_cb(topic,msg):                  # callback for debu
    print(msg)                          #debug
    if topic == b'esys/TBA/sensor/control1' and msg == b'upload':
        #uploadData()
        global payload
        client.publish('esys/TBA/sensor/data', payload)
        print("Data sent")
    elif topic == b'esys/time':
        strMsg = msg.decode('utf-8')    # decode byte to str
        dateAndTime = json.loads(strMsg)# decode JSON encoded time 
        global date
        dateString = dateAndTime["date"]
        date = parseDate(dateString)
        print(date)                     #debug
        print('set as system time')

client = MQTTClient(deviceName, brokerAddress)
client.set_callback(sub_cb)
#----------------------------------------Internal clock setup-------------------
rtc = RTC()

client.connect()
client.subscribe('esys/time')           #subscribe for time topic
client.wait_msg()                       #get time form server
client.disconnect()

rtc.datetime((date))                    #set internal clock to server time
#----------------------------------------RGB Sensor setup-----------------------
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = tcs34725.TCS34725(i2c)
sensor.gain(16)                         #gain: 1, 2, 16, 60 
#sensor.integration_time(402)           #change this for darker light conditions

def convert_rgb_data(raw_rgb):
    const = 255/1024                    #Convert 10 bit ADC data to 8 bit RGB
    raw_rgb = (  int(round(raw_rgb[0]*const, 0)), 
                 int(round(raw_rgb[1]*const, 0)),
                 int(round(raw_rgb[2]*const, 0)))
    return rgb2hsl.rgb2hsl(raw_rgb[0], raw_rgb[1], raw_rgb[2])
def getColorName(hsl):
    if (38<=hsl[0]<=61) and (30<=hsl[1]<=100):
        return 'Yellow'
    elif (80<=hsl[0]<=150) and (20<=hsl[1]<=60):
        return 'Green'
    elif (13<=hsl[0]<=36) and (30<=hsl[1]<=60):
        return 'Brown'
    else:
        return 'Non-valid banana', 0
def getRipeness(hsl):
    if (80<=hsl[0]<=150) and (20<=hsl[1]<=60):
        percent = int(round(100/116*(hsl[0]-80) + 39.6, 0))
        return percent
    elif (38<=hsl[0]<=61) and (30<=hsl[1]<=100):
        percent = int(round(100/116*(hsl[0]-38) + 19.8, 0))
        return percent
    elif (13<=hsl[0]<=36) and (30<=hsl[1]<=60):
        percent = int(round(100/116*(hsl[0]-13), 0))
        return percent
    else:
        return 0

#----------------------------------------Data reading and storing---------------
while True:
    if allowReadPin.value() == 1:           #If switch is on, read values
        s = sensor.read(True)               #Allow sensor read 
        raw_rgb = (s[0], s[1], s[2])
        hsl = convert_rgb_data(raw_rgb)     #Convert obtained data
        print(hsl)
        colorName = getColorName(hsl)
        ripeness = getRipeness(hsl)
        print(colorName)
        print(ripeness)
        payload = json.dumps({'HSL Data':{'H':hsl[0],'S':hsl[1],'L':hsl[2]},
                                'Banana color': colorName, 
                                'Ripeness': ripeness,
                                'Time': rtc.datetime()})

        #dataToUpload = open('JSONData.txt', 'a')
        #dataToUpload.write(payload)
        #dataToUpload.close()
        
        client.connect()                    #Connect to MQTT server
        client.subscribe('esys/TBA/sensor/control1')
        client.wait_msg()
        time.sleep_ms(100)
        client.disconnect()                 #Disconnect from the server
