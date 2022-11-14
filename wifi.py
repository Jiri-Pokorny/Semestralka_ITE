import network
import machine

sta_if = network.WLAN(network.STA_IF)
#ap_if = network.WLAN(network.AP_IF)

SSID = 'IoT-CIV'
key = 'UWBc9v.505.i0t'

sta_if.active(True)

def do_connect():
    #sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        try:
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(SSID, key)
            while not sta_if.isconnected():
                pass
        except:
            print("Exception occured")
            sta_if.connect(SSID, key)
            while not sta_if.isconnected():
                pass
    print('Connected: ', sta_if.isconnected())
    #print('network config:', sta_if.ifconfig())

#do_connect()