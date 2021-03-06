import network

labNetwork = 'EEERover'
labPassword = 'exhibition'

def connectWiFi(ssid, password):
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)                   # activate the interface
    if not wlan.isconnected():          # check if the station is connected
        wlan.connect(ssid, password)    # connect to an AP
        while not wlan.isconnected():
            print('.', end = '')
            time.sleep_ms(500)
    wlan.config('mac')                  # get the interface's MAC adddress

    print('Network is connected. Config:', wlan.ifconfig())

connectWiFi(labNetwork, labPassword)    # connect to WiFi network
