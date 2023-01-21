import thermometer
import wifi
import publisher
import machine
from machine import RTC
import ntptime
import time
import json
import network
import sys


class Main:
    
    def __init__(self) -> None:
        print("main - init...")
        self.TEAM = 'black'
        self.MEASUREMENTS = 6
        self.last_time_set = 0
        self.thermometer = thermometer.Thermometer()
        self.wifi = wifi.Wifi()
        self.publisher = publisher.Publisher()
        self.rtc = machine.RTC()        

    def wifi_connect(self):
        print("main - wifi_connect...")
        self.wifi.get_network_data()
        self.wifi.do_connect()
        return 0

    def init_time(self):
        print("main - init_time...")
        try:
            ntptime.settime()
            self.last_time_set = self.rtc.datetime()[4]
            return 0
        except Exception:
            sys.exit()

    def time_synchro(self):
        print("main - time_synchro...")
        now = self.rtc.datetime()
        if self.last_time_set != now[4]:
            ntptime.settime()
            self.last_time_set = now[4]
            print("Clock synchronization...")
        return now

    def get_temperature(self):
        print("main - get_temperature...")
        temperature = 0
        for i in range(self.MEASUREMENTS):
            temperature += self.thermometer.measure()
            print("Measuring temperature...")
            time.sleep(55/self.MEASUREMENTS)
        temperature = temperature/self.MEASUREMENTS
        return temperature

    def generate_publisher_message(self, temperature, now):
        print("main - generate_publisher_message...")
        timestamp = "{year:0>4}-{month:0>2}-{day:0>2}T{hour:0>2}:{minute:0>2}:{second:0>2}.{millisecond:0>6}".format(year=now[0], month=now[1], day=now[2], hour=(now[4]), minute=now[5], second=now[6], millisecond=now[7])
        #put together a message
        message = json.dumps({'team_name': self.TEAM, 'timestamp': timestamp, 'temperature': round(temperature, 2)})
        self.publisher.publish(message)
        print("publishing...")
        print(message)
        return 0

# Publish message
m = Main()
m.wifi_connect()
m.init_time()
while True:
    try:
        m.wifi.do_connect()
        # get temperature
        temperature = m.get_temperature()
        # get time
        now = m.time_synchro()
        m.generate_publisher_message(temperature, now)
    except Exception as e:
        machine.reset()



   