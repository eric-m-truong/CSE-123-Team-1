# Code taken and adapted from:
# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

import paho.mqtt.client as mqtt
from random import randrange, uniform
from datetime import datetime
import time

mqttBroker = input("Broker IP: ")
client_id = input("Enter an ID: ")

client = mqtt.Client(client_id)  # Initialize
client.connect(mqttBroker)  # I think this assumes the default port

topic = input("Topic: ")

while True:
    randNumber = uniform(20.0, 21.0)
    message = str(datetime.now()) + ", " + client_id + ", " + str(randNumber)
    client.publish(topic, message)
    print(str(topic) + ": " + message)
    time.sleep(1)
