import network
import machine
import time
import sys
import AP

class Wifi:

    def __init__(self) -> None:
        print("WifiHome - init...")
        self.access_point = AP.AP()
        self.access_point.ap.active(False)
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.SSID = ""
        self.KEY = ""

    def get_network_data(self):
        print("WifiHome - get_network_data...")
        try:
            with open('network.txt') as f:
                lines = f.readlines()
                self.SSID = str(lines[0]).strip()
                self.KEY = str(lines[1]).strip()
            return 0
        except Exception:
            self.access_point.run()
            self.get_network_data()
            
    def do_connect(self):
        print("WifiHome - do_connect...")
        try:
            #sta_if = network.WLAN(network.STA_IF)
            count = 0
            while not self.sta_if.isconnected():
                print('connecting to network...', self.SSID, self.KEY)
                self.sta_if.active(True)
                self.sta_if.connect(self.SSID, self.KEY)
                if count > 60:
                    machine.reset()
                    # run AP and get wifi network info
                count += 1
                time.sleep(0.5)
            print('Connected: ', self.sta_if.isconnected())
            return 0
        except Exception:
            machine.reset()