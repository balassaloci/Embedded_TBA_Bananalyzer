# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import network
import time

#wlan = network.WLAN(mode=network.WLAN.AP)
#wlan.init(mode=network.WLAN.AP, ssid='tba', auth=(network.WLAN.WPA2,'www.wipy.io'), channel=7, antenna=network.WLAN.INT_ANT)


#webrepl.start()
gc.collect()

