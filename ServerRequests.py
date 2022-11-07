# HTTP Challenge - player initialization
# choose your username and password (config.yml)
# you might need to: $ pip install pyyaml
# call this cell once at the beginning

from requests import post, get, delete, HTTPError
from json import JSONDecodeError
import json
from yaml import full_load as yaml_load
from datetime import datetime

URI_BASE = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
LOGIN_URL = URI_BASE+'/login'
SENSOR_URL = URI_BASE+'/sensors'
MEASUREMENT_URL = URI_BASE+'/measurements'
ALERT_URL = URI_BASE+'/alerts'

sensors = {'19': '610eb3d2-d48d-47b0-ba4e-5e04f5c55c80'}

# posts the request to the given url
# if successfull, returns response
# url - string value (url address of the server)
# body - dictionary/json (body of the request)
# json - json (body of the request (create_measurement))
# head - dictionary/json (header of the request)
def post_(url, body, json, headers):
    try:
        response = post(url=url, data=body, json=json, headers=headers)

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

# sends a get request to the given url
# if successfull, returns response
# url - string value (url address of the server)
# body - dictionary/json (body of the request)
# head - dictionary/json (header of the request)
def get_(url, body, head):
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

# sends a delete command to the given url
# if successfull, returns response
# url - string value (url address of the server)
# header - dictionary/json (header of the request)
def del_(url, header):
    try:
        response = delete(url, headers=header)

        if response.status_code == 200:
            try:
                print("Successfully deleted")
                return response
            except JSONDecodeError:
                print('E: Response is not of JSON format.')
                return {}
        else:
            print('E: Not available, try again. Status code:', response.status_code)
            print_reply(response.json())
            return {}
    except HTTPError as http_err:
        print('E: HTTP error occurred:', http_err)

# prints the response to console
# 2 parts of the response
#   key - name of the value
#   value - given value
def print_reply(reply):
    for k, v in reply.items():
        print(str(k)+': '+str(v)+'\n')

# logs into the cloud server
# sets the global variable team_UUID
def login():
    login_headers = {'Content-Type':'application/json'}
    login_body = json.dumps({"username": "Black","password": "S5@y1&00"})
    response = post_(url=LOGIN_URL, body=login_body, json=None, headers=login_headers)
    print_reply(response)
    global team_UUID
    team_UUID = response["teamUUID"]

# reads data from all sensors and prints it
def read_all_sensors():
    read_all_sensors_header = {'teamUUID': team_UUID}
    read_all_sensors_body = {}
    response = get_(SENSOR_URL, read_all_sensors_body, read_all_sensors_header)
    print_reply(response[0])

# reads information about a single sensor
def read_sensor_by_id(id):
    read_sensor_by_id_header = {'teamUUID': team_UUID}
    read_sensor_by_id_body = {}
    response = get_(SENSOR_URL+'/'+str(id),read_sensor_by_id_body,read_sensor_by_id_header)
    print_reply(response)

# calls read all sensors
# takes the sensorUUID and name from the response
# fills the global variable sensor_UUID
def get_all_sensors():
    read_all_sensors_header = {'teamUUID': team_UUID}
    read_all_sensors_body = {}
    response = get_(SENSOR_URL, read_all_sensors_body, read_all_sensors_header)
    for sensor in response:
        sensors[str(sensor['id'])] = sensor['sensorUUID']

# gets all measurements for all known sensors
# known sensors are all sensors in the sensors dictionary
def read_all_measurements():
    for sensor in sensors:
        print(sensor)
        read_all_measurements_parameter = "?sensorUUID="+sensors[sensor]
        read_all_measurements_header = {'teamUUID': team_UUID}
        read_all_measurements_body = {}
        response = get_(MEASUREMENT_URL+read_all_measurements_parameter, read_all_measurements_body, read_all_measurements_header)
        for measurement in response:
            print_reply(measurement)

# gets single measurement reading
# prints the result
# id - int value (id of the measurement)
def read_measurement_by_id(id):
    read_by_id_parameter = '/'+str(id)
    read_by_id_body = {}
    read_by_id_header = {'teamUUID': team_UUID}
    result = get_(MEASUREMENT_URL+read_by_id_parameter, read_by_id_body, read_by_id_header)
    print_reply(result)

# deletes measurement with a given id
# id - int value (id of the measurement)
def delete_measurement_by_id(id):
    delete_by_id_parameter = '/'+str(id)
    delete_by_id_header = {'teamUUID': team_UUID}
    response = del_(MEASUREMENT_URL+delete_by_id_parameter, delete_by_id_header)
    print(response)

# posts a measurement to the server, prints the result
# what parameters should this have?
# should we perform valid input  check?
def create_measurement(sensor, temperature, status):
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
    print("timestamp: ", time_stamp)
    response = post_(url=MEASUREMENT_URL, body=None, json=create_measurement_body, headers=create_measurement_header)
    print_reply(response)

# gets all alerts from server
# prints all the recieved alerts
def read_all_alerts():
    read_all_alerts_header = {'teamUUID': team_UUID}
    read_all_alerts_body = {}
    response = get_(ALERT_URL, read_all_alerts_body, read_all_alerts_header)
    for alert in response:
        print_reply(alert)

# get the alert by id
# id - int value (id of the alert)
def read_alert_by_id(id):
    read_by_id_parameter = '/'+str(id)
    read_by_id_header = {'teamUUID': team_UUID}
    read_by_id_body = {}
    response = get_(ALERT_URL+read_by_id_parameter, read_by_id_body, read_by_id_header)
    print_reply(response)

# creates an alert
# id - int value (id of the sensor)
# temp - float value (measured temperature)
# lowTemp - float value (lowest acceptable temperature)
# highTemp - float value (highest acceptable temperature)
def create_alert(id, temp, lowTemp, hightTemp):
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

# deletes alert by alert id
# id - int value (alert id)
def delete_alert(id):
    delete_alert_header = {'teamUUID': team_UUID}
    delete_alert_body = {}
    response = del_(ALERT_URL+'/'+str(id), delete_alert_body,delete_alert_header)
    print_reply(response)

print("login...")
login()
print("team_UUID:"+ team_UUID)
print("read all sensors...")
read_all_sensors()
print('read sensor 19...')
read_sensor_by_id(19)
print('creating alert...')
create_alert(19, 70, 10, 35)
print('read alert 7671...')
read_alert_by_id(7671)
#print("sensors: ", sensors)
#print("read all measurements...")
#read_all_measurements()
#print("create measurement...")
#print("sensor: ", sensors['sensor18_Black'])
#create_measurement(sensors['sensor18_Black'],10.2,'TEST')
#print("read all measurements...")
#read_all_measurements()
#print("read all alerts...")
#read_all_alerts()
#print("read alert by id...")
#read_alert_by_id(7671)
#print("delete measurement by id...")
#delete_measurement_by_id(676541)