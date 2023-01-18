#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Requirements
'''

from google.cloud import bigquery
from google.oauth2 import service_account
import json
import time
import os
import paho.mqtt.client as mqtt
from json import dumps as dumps_json
from requests import post, get, delete, HTTPError
from json import JSONDecodeError
import json
from datetime import datetime


# In[2]:


'''
BQ credentials
'''

bq_credentials =  service_account.Credentials.from_service_account_file('/Users/BS/Desktop/FAV/ITE/archetix-data-squad-5918f5b48840.json')
client_bq = bigquery.Client(credentials=bq_credentials, project=bq_credentials.project_id)
dataset_id = 'baru_skola'
table_ref = client_bq.dataset(dataset_id).table('test_1')
table = client_bq.get_table(table_ref)

'''
AIMTEC
'''
URI_BASE = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
LOGIN_URL = URI_BASE+'/login'
SENSOR_URL = URI_BASE+'/sensors'
MEASUREMENT_URL = URI_BASE+'/measurements'
ALERT_URL = URI_BASE+'/alerts'
USERNAME = "Black"
PASSWORD = "S5@y1&00"

'''
MQTT BROKER
'''
BROKER_IP = '147.228.124.230'
BROKER_PORT = 1883
BROKER_UNAME = 'student'
BROKER_PASSWD = 'pivotecepomqtt' 
TOPIC = 'ite/#'
team_UUID = '5902f2ec-d62b-4c7a-8d40-2875c426edf6'
sensors = {'19': '610eb3d2-d48d-47b0-ba4e-5e04f5c55c80'}
sensorID = 19
sensorUUID = '610eb3d2-d48d-47b0-ba4e-5e04f5c55c80'
minTemperature = 0.0
maxTemperature = 24.0


# In[5]:


def read_all_sensors():
    '''
    reads all sensors information
    :return response[0]:
    '''
    read_all_sensors_header = {'teamUUID': team_UUID}
    read_all_sensors_body = {}
    response = get_(SENSOR_URL, read_all_sensors_body, read_all_sensors_header)
    print_reply(response[0])
    return response[0]


def post_(url, body, json, headers):
    '''
    posts a get request to the given url if successful, returns response
    :param url:
    :param body:
    :param json:
    :param headers:
    :return:
    '''
    try:
        response = post(url=url, data=body, json=json, headers=headers)

        if response.status_code == 200:
            try:
                return response.json()
            except JSONDecodeError:
                print('E: Response is not if JSON format.')
                return {}
        else:
            print('E: Not available, try again. Status code:', response.status_code)
            return {}
    except HTTPError as http_err:
        print('E: HTTP error occurred:', http_err)


def get_(url, body, head):
    '''
    sends a get request to the given url if successful, returns response
    :param url:
    :param body:
    :param head:
    :return:
    '''
    try:
        response = get(url, body, headers=head)

        if response.status_code == 200:
            try:
                return response.json()
            except JSONDecodeError:
                print('E: Response is not of JSON format.')
                return {}
        else:
            print('E: Not available, try again. Status code:', response.status_code)
            return {}
    except HTTPError as http_err:
        print('E: HTTP error occurred:', http_err)



def print_reply(reply):
    '''
    prints the reply to console
    2 parts of the response
    key - name of the value
    value - given value
    :param reply:
    :return:
    '''
    
    for k, v in reply.items():
        print(str(k)+': '+str(v)+'\n')

def login():
    '''
    logs into the cloud server
    sets the global variable team_UUID
    :return:
    '''
    login_headers = {'Content-Type':'application/json'}
    login_body = json.dumps({"username": USERNAME,"password": PASSWORD})
    response = post_(url=LOGIN_URL, body=login_body, json=None, headers=login_headers)
    print(response)
    testUUID = response["teamUUID"]

    if testUUID  == None:
        time.sleep(60)
        response = post_(url=LOGIN_URL, body=login_body, json=None, headers=login_headers)
        testUUID = response["teamUUID"]
        if testUUID == None:
            print('Not connected to AIMTEC!')


def create_measurement(sensor, temperature, status):
    '''
    Creates measurement and sends it to AIMTEC
    :param sensor:
    :param temperature:
    :param status:
    :return:
    '''
    print('creating measument')
    # timestamp in postman is in ISO 8601 format
    time = str(datetime.now())[0:(len(str(datetime.now()))-3)]
    time_stamp = str(time).split(" ")[0]+"T"+str(time).split(" ")[1]+"+01:00"
    create_measurement_header = {'teamUUID': str(team_UUID), 'Content-Type': 'application/json'}
    create_measurement_body = {
		"createdOn": str(time_stamp),
		"sensorUUID": str(sensor),
		"temperature": str(temperature),
		"status": str(status)
        }
    #print("timestamp: ", time_stamp)
    response = post_(url=MEASUREMENT_URL, body=None, json=create_measurement_body, headers=create_measurement_header)
    print(response)

def create_alert(id, temp, lowTemp, hightTemp):
    '''
    Creates alert if temperature is not within bounds
    :param id:
    :param temp:
    :param lowTemp:
    :param hightTemp:
    :return:
    '''
    print('creating_alert')
    time = str(datetime.now())[0:(len(str(datetime.now()))-3)]
    time_stamp = str(time).split(" ")[0]+"T"+str(time).split(" ")[1]+"+01:00"
    create_alert_header = {'teamUUID': team_UUID, 'Content-Type': 'application/json'}
    create_alert_body = {
		"createdOn": time_stamp,
		"sensorUUID": sensors[str(id)],
		"temperature": str(temp),
		"lowTemperature": str(lowTemp),
		"highTemperature": str(hightTemp)
	}
    response = post_(url=ALERT_URL,body=None, json=create_alert_body, headers=create_alert_header)
    print_reply(response)


# In[6]:


def on_connect(client, userdata, mid, qos):
    '''
    Subscribing in on_connect() means that if we lose the connection and
    reconnect then subscriptions will be renewed.
    :param client:
    :param userdata:
    :param mid:
    :param os:
    :return:
    '''
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    '''
    Sends data to Aimtec and BigQuery on message
    :param client:
    :param userdata:
    :param msg:
    :return:
    '''
    if (msg.payload == 'Q'):
        client.disconnect()
    msg.payload = msg.payload.decode("utf-8")
    mess = msg.payload 
    try:
        zprava = json.loads(mess)
    except:
        print("cant load message")
        return
    #print(zprava["team_name"])
    if zprava["team_name"] == 'black':
        try:
            to_aimtec(zprava)
        except Exception as e: 
            print("Cant't load to AIMTEC, error message: ",e)
        
        
    try:
        to_bq(mess)
    except:
        print("can't load to BQ")
        
    try:
        team = zprava["team_name"]
        content = {}
        content["date"] = str(datetime.now().date())
        content["time"] = str(datetime.now().time())
        last_activity[team] = content
        print(last_activity)
        print(type(last_activity))
            
        with open("last_activity.json", "w") as outfile:
            json.dump(last_activity,outfile)
       
    except Exception as e:
        print ("wrong message format to store",e)

def to_aimtec(zprava):
    '''
    Sends data to Aimtec
    :param zprava:
    :return:
    '''
    temperature = zprava["temperature"]
    print(temperature)
    try:
        create_measurement(sensorUUID, temperature, "OK")
    except:
        ("to_aimtec_error")
        
    if temperature < minTemperature or temperature > maxTemperature:
        print("extreme_temperature")
        try:
            create_alert(19, temperature, minTemperature, maxTemperature)
        except:
            print("alert_error")
        


def to_bq(msg):
    '''
    Sends data to BigQuery database
    :param msg:
    '''
    json_str = json.loads(msg)
    errors = client_bq.insert_rows_json(table,[json_str])
    if errors == []:
        print("New rows have been added to BQ.")
        print(msg)
    else:
        print("Encountered errors while inserting rows to BQ: {}".format(errors))


# In[40]:


if __name__ == '__main__':
    '''
    main function
    '''
    with open('last_activity.json') as json_file:
        last_activity = json.load(json_file)

    
    login()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(BROKER_UNAME, password=BROKER_PASSWD)
    client.connect(BROKER_IP, BROKER_PORT, 60)

    client.loop_forever()


# In[60]:


from datetime import timedelta
str((datetime.now() + timedelta(hours=1)).time())


# In[9]:


temp = 10
create_alert(19, temp, minTemperature, maxTemperature)


# In[ ]:





# In[ ]:




