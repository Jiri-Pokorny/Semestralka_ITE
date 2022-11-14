import network
import machine
import logger

sta_if = network.WLAN(network.STA_IF)
#ap_if = network.WLAN(network.AP_IF)

SSID = 'asy-wifihome'
key = 'passw0rd'

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
                machine.reset()
            count += 1
        print('Connected: ', sta_if.isconnected())
        #print('network config:', sta_if.ifconfig())
    except Exception as e:
        logger.log("WiFi exception: "+str(e))
        sys.exit()
#do_connect()