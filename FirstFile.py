# HTTP Challenge - player initialization
# choose your username and password (config.yml)
# you might need to: $ pip install pyyaml
# call this cell once at the beginning
'''
from requests import post, HTTPError
from json import JSONDecodeError
import json
from yaml import full_load as yaml_load

URI_BASE = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
EP_LOGIN = URI_BASE+'/login'
EP_MEASUREMENT = URI_BASE+'/measurements'
EP_ALERT = URI_BASE+'/alerts'
EP_SENSOR = URI_BASE+'/sensors'



def print_reply(reply):
    for k, v in reply.items():
        print(str(k)+': '+str(v)+'\n')

def post_(ep, body, headers):
    #body.update(login_credentials)
    try:
        response = post(ep, body, headers=headers)

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

def login():
    header = {"Content-Type":"application/json"}

    login_credentials = json.dumps({
        'username': 'Orange',
        'password': 'Kv7Af59^'
    })
    print_reply(reply = post_(ep=(URI_BASE+EP_LOGIN), body=login_credentials, headers=header))

#print(f'Initialized. Config file loaded. Player {login_credentials["username"]} ready to log in.')a

login()
'''

from requests import post,get,delete, HTTPError
from json import JSONDecodeError
import json
from json import dump

URI_BASE = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
LOGIN_url = URI_BASE+'/login'
Sensor_url = URI_BASE+'/sensors'
Measurements_url =URI_BASE+'/measurements'
data_green = {}
sensor_list=[]
response_num=500

def print_reply(reply):
    for k, v in reply.items():
        print(str(k)+': '+str(v)+'\n')
        data_green[str(k)] = str(v)
        


def post_(ep, body,headers):
    try:
        response = post(ep, body,headers=headers)

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
        
        

def get_(ep,params,headers):
    try:

        response = get(ep,params=params,headers=headers)

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
        
def del_(ep,params,headers):
    try:
        #del mozna neni dobre jmeno 
        response = delete(ep,params=params,headers=headers)

        if response.status_code == 200:
            try:
                return response.json()
            except JSONDecodeError:
                return response.status_code
        else:
            print('E: Not available, try again. Status code:', response.status_code)
            return response.status_code

    except HTTPError as http_err:
        print('E: HTTP error occurred:', http_err)
        return response.status_code

def login(body):
    h={'Content-Type':"application/json"}
    print_reply(reply=post_(ep=LOGIN_url, body=body,headers=h))
    
def createMeasurements(sensorUUID,teamUUID,date,temperature,status):
    ## WORK IN PROGRESS
    bodyCr=json.dumps({
        "createdOn": date,
        "sensorUUID": sensorUUID,
        "temperature": temperature,
        "status": status
    })
    print(bodyCr)
    h={'teamUUID': teamUUID,'Content-Type':"application/json"}
    print_reply(reply=post_(ep=Measurements_url, body=bodyCr,headers=h))
    
def readAllSensors(teamUUID):
    h={'teamUUID': teamUUID}
    sensor_list=get_(ep=Sensor_url,params=None,headers=h)
    #print(sensor_list)
    return sensor_list

def readAllMeasurements(sensorUUID, teamUUID):
    h={'teamUUID': teamUUID}
    measurements_list=[]
    measurements_list = get_(ep=Measurements_url ,params =None,headers = h)
    return measurements_list

def deleteMeasurementByID(teamUUID,MeasurementID):
    Del_Measurement_id =  Measurements_url+'/'+str(MeasurementID)
    h={'teamUUID': teamUUID}
    response_num=del_(ep = Del_Measurement_id, params=None,headers=h)
    if response_num ==200:       
        print("Succcesfuly deleted measurement: "+str(MeasurementID)+".")
    else:
        print("Something went wrong while deleting measurement: " +str(MeasurementID)+ ". Site response was: "+ str(response_num))

body = json.dumps({"username": "Black",
    "password": "S5@y1&00"})   
login(body)