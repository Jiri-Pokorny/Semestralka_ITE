import paho.mqtt.client as mqtt
from json import dumps as dumps_json
import time

BROKER_IP = '147.228.124.230'
BROKER_PORT = 1883
BROKER_UNAME = 'student'
BROKER_PASSWD = 'pivotecepomqtt'
TOPIC = 'ite/black/test/'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, mid, qos):
    print('Connected with result code qos:', str(qos))

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print('On publish mid: ', str(mid))

def send2broker(client, topic, payload, qos=0, retain=False):
    client.publish(topic, payload, qos=qos, retain=False)

def init_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.username_pw_set(BROKER_UNAME, password=BROKER_PASSWD)
    client.connect(BROKER_IP, BROKER_PORT, 60)
    return client

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.username_pw_set(BROKER_UNAME, password=BROKER_PASSWD)
    client.connect(BROKER_IP, BROKER_PORT, 60)
    i = 0
    while True:
        print("send2broker", i)
        send2broker(client, TOPIC, dumps_json({'team_name': 'black', 'timestamp': '2020-03-24T15:26:05.336974', 'temperature': 25.72}))
        i += 1
        time.sleep(3)
    client.disconnect()
