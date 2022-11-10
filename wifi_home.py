import network
import sys
import logger

sta_if = network.WLAN(network.STA_IF)
#ap_if = network.WLAN(network.AP_IF)

SSID = 'asy-wifihome'
key = 'passw0rd'

sta_if.active(True)

def do_connect():
    try:
        #sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(SSID, key)
            while not sta_if.isconnected():
                pass
        print('Connected: ', sta_if.isconnected())
        #print('network config:', sta_if.ifconfig())
    except Exception as e:
        logger.log("WiFi exception: ", e)
        sys.exit()
#do_connect()