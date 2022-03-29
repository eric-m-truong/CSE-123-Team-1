# Code taken and adapted from:
# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

import paho.mqtt.client as mqtt
from random import randrange, uniform
from datetime import datetime
import time
import sys

# Arguments
argc = len(sys.argv)
if (argc < 4):
    print("Usage:", sys.argv[0], "<broker_ip> <client_id> <mqtt_topic>")
    sys.exit(-1)

# mqttBroker = input("Broker IP: ")
# client_id = input("Enter an ID: ")

mqttBroker = sys.argv[1]
client_id = sys.argv[2]
topic = sys.argv[3]

client = mqtt.Client(client_id)  # Initialize
client.connect(mqttBroker)  # I think this assumes the default port

# topic = input("Topic: ")

while True:
    randNumber = uniform(20.0, 21.0)
    message = str(datetime.now()) + ", " + client_id + ", " + str(randNumber)
    client.publish(topic, message)
    print(str(topic) + ": " + message)
    time.sleep(1)
