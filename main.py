import thermometer
#import wifi
import wifi_home as wifi
import publisher_micro as publisher
import machine
from machine import RTC
import ntptime
import time
import json
import network
import sys

# variables
team_name = 'black'
rtc = machine.RTC()
try:
    wifi.do_connect()
    measurements = 6

    ntptime.settime()
    lastTimeSet = rtc.datetime()[4]
except Exception as e:
    print(e)
    sys.exit()

# Publish message
while True:
    try:
        # get temperature
        temperature = 0
        for i in range(measurements):
            temperature += thermometer.measure()
            print("Measuring temperature...")
            time.sleep(55/measurements)
        temperature = temperature/measurements
        # get time
        now = rtc.datetime()
        if lastTimeSet != now[4]:
            ntptime.settime()
            lastTimeSet = now[4]
            print("Clock synchronization...")
        print("datetime: ",now)
        #timestamp = "{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}.{:0>6}".format(now[0],now[1],now[2],(now[4])%24,now[5],now[6],now[7])
        timestamp = "{year:0>4}-{month:0>2}-{day:0>2}T{hour:0>2}:{minute:0>2}:{second:0>2}.{millisecond:0>6}".format(year=now[0], month=now[1], day=now[2], hour=(now[4]), minute=now[5], second=now[6], millisecond=now[7])
        #print('timestamp: ', timestamp)
        #put together a message
        message = json.dumps({'team_name': team_name, 'timestamp': timestamp, 'temperature': round(temperature, 2)})
        # if not connected to the wifi, connect
        wifi.do_connect()
        # send the message
        publisher.publish(message)
        # wait for X seconds before looping
    except Exception as e:
        machine.reset()



   