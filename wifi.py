import network
import machine
import time
import sys

sta_if = network.WLAN(network.STA_IF)
#ap_if = network.WLAN(network.AP_IF)

SSID = 'IoT-CIV'
key = 'UWBc9v.505.i0t'

sta_if.active(True)

def do_connect():
    try:
        #sta_if = network.WLAN(network.STA_IF)
        count = 0
        while not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(SSID, key)
            if count > 100:
                sys.exit()
            count += 1
            time.sleep(0.1)
        print('Connected: ', sta_if.isconnected())
    except Exception as e:
        print("WiFi exception ",e)
        machine.reset()
    #print('network config:', sta_if.ifconfig())
#do_connect()