from turtle import onclick
import thermometer
import wifi
import publisher

import paho.mqtt.client as mqtt
import time
from json import json

# WIFI connection
wifi.do_connect()

# variables
team_name = 'black'
client = publisher.init_client()

# Publish message
while True:
    temperature = thermometer.measure()
    timestamp = str(time.now().isoformat())
    message = json.dumps({'team_name': team_name, 'timestamp': timestamp, 'temperature': temperature})
    publisher.send2broker(client, publisher.TOPIC, message)