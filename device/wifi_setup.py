import network
import time

wlan = network.WLAN(mode=WLAN.AP)
wlan.init(mode=WLAN.API, ssid='tba', auth=(WLAN.WPA2, 'pisiskaki'), channel=7, antenna=WLAN.INT_ANT)


