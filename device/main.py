import tcs34725
import rgb2hsl
import json
import time
from machine import I2C, Pin, unique_id, RTC
from umqtt.simple import MQTTClient

date = 0, 0, 0, 0, 0, 0, 0, 0           # set global variables for date and
#----------------------------------------I/O pins-------------------------------
allowReadPin = Pin(14, Pin.IN, None)    # Switch input pin14 without pull res.
#----------------------------------------RGB Sensor setup-----------------------
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = tcs34725.TCS34725(i2c)
sensor.gain(16)                         #gain: 1, 2, 16, 60
#----------------------------------------Data processing------------------------
def convert_rgb_data(raw_rgb):          #Convert 10 bit ADC data to 8 bit RGB
    const = 255/1024
    raw_rgb = (int(round(raw_rgb[0]*const, 0)),
               int(round(raw_rgb[1]*const, 0)),
               int(round(raw_rgb[2]*const, 0)))
    return rgb2hsl.rgb2hsl(raw_rgb[0], raw_rgb[1], raw_rgb[2])

def getColorName(hsl):                  #Convert HSL code to colour names
    if (80<=hsl[0]<=150) and (20<=hsl[1]<=60):
        return 'Green'
    elif (40<=hsl[0]<=61) and (30<=hsl[1]<=100):
        return 'Yellow'                 #ranges are based on empirical data
    elif (13<=hsl[0]<=39) and (20<=hsl[1]<=60):
        return 'Brown'
    else:
        return 'Non-valid banana'

def getRipeness(hsl):                   #map the used colour range to % 
    if (80<=hsl[0]<=150) and (20<=hsl[1]<=60):      #green
        percent = 100-int(round(100/117*(hsl[0]-80) + 40.1, 0))
        return percent
    elif (40<=hsl[0]<=61) and (30<=hsl[1]<=100):    #yellow
        percent = 100-int(round(100/117*(hsl[0]-40) + 22.2, 0))
        return percent
    elif (13<=hsl[0]<=39) and (20<=hsl[1]<=60):     #brown
        percent = 100-int(round(100/117*(hsl[0]-13), 0))
        return percent
    else:
        return 0
#----------------------------------------Taking measurement---------------------
def takeMeasurement():
    s = sensor.read(True)               #Get sensor reading
    raw_rgb = (s[0], s[1], s[2])
    hsl = convert_rgb_data(raw_rgb)     #Convert obtained data
    print("H: %i, S: %i, L: %i"  %(hsl[0],hsl[1],hsl[2]))
    colorName = getColorName(hsl)
    print("Banana colour: " + colorName)
    ripeness = getRipeness(hsl)
    print("Ripeness: %i %%" %(ripeness,))
    #convert data to JSON before uploading it to server
    payload = json.dumps({'HSL Data':{'H':hsl[0],'S':hsl[1],'L':hsl[2]},
                            'Banana color': colorName,
                            'Ripeness': ripeness,
                            'Time': rtc.datetime()})
    return payload
#----------------------------------------Date parser----------------------------
def parseDate(a):
    return  int(a[0:4]), int(a[5:7]),   \
            int(a[8:10]), int(a[11:13]),\
            int(a[14:16]), int(a[17:19]), 0, 0
#----------------------------------------MQTT client setup----------------------
def sub_cb(topic,msg):                  # callback for wait_msg()
    print("Message received: "+msg.decode('utf-8'))
    if topic == b'esys/TBA/sensor/control1' and msg == b'upload':
        payload = takeMeasurement()
        client.publish('esys/TBA/sensor/data', payload)
        print("Data sent")
    elif topic == b'esys/time':
        strMsg = msg.decode('utf-8')    # decode byte to str
        dateAndTime = json.loads(strMsg)# decode JSON encoded time 
        global date
        dateString = dateAndTime["date"]
        date = parseDate(dateString)
        print("System date set to: %i-%i-%i %i:%i:%i" % (date[0],date[1],
                                                         date[2],date[3],
                                                         date[4],date[5],))

deviceName = 'esp8266_' + str(unique_id(), 'utf-8')
brokerAddress = '192.168.0.10'
client = MQTTClient(deviceName, brokerAddress)
client.set_callback(sub_cb)
#----------------------------------------Internal clock setup-------------------
rtc = RTC()

client.connect()
client.subscribe('esys/time')           #subscribe for time topic
print("Waiting for time data from server...")
client.wait_msg()                       #get time form server
client.disconnect()

rtc.datetime((date))                    #set internal clock to server time
#----------------------------------------Data reading and storing---------------
while True:
    if allowReadPin.value() == 1:       #If switch is on, read values
        client.connect()                #Connect to MQTT server
        client.subscribe('esys/TBA/sensor/control1')
        client.wait_msg()               #wait for 'upload' message from server
        client.disconnect()             #Disconnect from the server
