from umqtt.simple import MQTTClient as mqtt
from json import dumps as dumps_json
import time
import sys
import machine

BROKER_IP = '147.228.124.230'
BROKER_PORT = 1883
BROKER_UNAME = 'student'
BROKER_PASSWD = 'pivotecepomqtt'
TOPIC = 'ite/black/test/'
CLIENT_ID = 'ESP8266_Black'

def publish(data):
    try:
        client = mqtt(CLIENT_ID, BROKER_IP,port=BROKER_PORT, user=BROKER_UNAME, password=BROKER_PASSWD)
        client.connect()
        client.publish(TOPIC, data) 
    except Exception as e:
        machine.reset()
