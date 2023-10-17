import paho.mqtt.client as mqtt
import requests
from andondjango.settings import *
import json
import datetime


# mqttServer = "localhost"
# mqttPort = 1883
# mqttKeepAlive = 60
#
# httpHost = "localhost"
# httpPort = 8000

andonResponsePublish = "andonResponse"
andonSubscribe = "andon/#"

requestList = ["POST","GET","DELETE","PUT","PATCH"]


# from Andon.models import LiveData, MachineDetail, MQTTConfig, MachineError, TechnicianDetail


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(andonSubscribe)
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    currentTopic = msg.topic.split("/")
    currentMessage = msg.payload
    # print (currentTopic)
    # if currentTopic[0] != "andon":
    #     print ("Message error-"+str(currentTopic[0]))
    #     client.publish(andonResponsePublish, "Andon Topic Error")
    #     return

    requestMethod = str(currentTopic[1]).upper()
    if  requestMethod not in requestList:
        print ("Method Error--"+requestMethod)
        client.publish(andonResponsePublish, "Method Error")
        return

    httpurl = 'http://'+httpHost+":"+str(httpPort)+"/"+"/".join(currentTopic[2:])
    headers = {'content-type': 'application/json; charset=UTF-8'}


    if httpurl[-1] != '/':
        httpurl = httpurl + '/'

    print (httpurl)

    if requestMethod == 'GET':
        httpResponse = requests.get(httpurl)

    elif requestMethod == 'POST':
        httpResponse = requests.post(httpurl,data=currentMessage,headers = headers)
        # print (httpResponse.status_code)
        # print (httpResponse.text)

    elif requestMethod == 'PUT':
        httpResponse = requests.put(httpurl,data=currentMessage,headers = headers)
        # print (httpResponse.status_code)
        # print (httpResponse.text)

    elif requestMethod == 'DELETE':
        httpResponse = requests.delete(httpurl,data=currentMessage,headers = headers)
        # print (httpResponse.status_code)
        # print (httpResponse.text)

    print (httpResponse.status_code)
    print (httpResponse.text)
    client.publish(andonResponsePublish, httpResponse.text)


try:
    # mqttconfig = MQTTConfig.objects.get(MQTT_ID=1)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("","")
    client.connect(
        host=mqttServer,
        port=mqttPort,
        keepalive=mqttKeepAlive
    )

except Exception as e:
    print (e)
    # print("Add server details in the MQTT configs table")
    # client = mqtt.Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.username_pw_set("", "")
    # client.connect(
    #     host=mqttServer,
    #     port=mqttPort,
    #     keepalive=mqttKeepAlive
    # )

