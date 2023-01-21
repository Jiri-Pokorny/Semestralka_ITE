from umqtt.simple import MQTTClient as mqtt
from json import dumps as dumps_json
import time
import sys
import machine

class Publisher:

    def __init__(self) -> None:
        print("Publisher - init...")
        self.BROKER_IP = '147.228.124.230'
        self.BROKER_PORT = 1883
        self.BROKER_UNAME = 'student'
        self.BROKER_PASSWD = 'pivotecepomqtt'
        self.TOPIC = 'ite/black/'
        self.CLIENT_ID = 'ESP8266_Black'

    def publish(self, data):
        print("Publisher - publish...")
        try:
            client = mqtt(self.CLIENT_ID, self.BROKER_IP,port=self.BROKER_PORT, user=self.BROKER_UNAME, password=self.BROKER_PASSWD)
            client.connect()
            client.publish(self.TOPIC, data)
            return 0 
        except Exception:
            machine.reset()
