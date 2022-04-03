#!/usr/bin/python3

# Code taken and adapted from:
# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

import paho.mqtt.client as mqtt
from random import uniform
import time
import sys

# Arguments
argc = len(sys.argv)
if (argc < 3):
    print("Usage:", sys.argv[0], "<broker_ip> <mac_address>")
    sys.exit(-1)

mqttBroker = sys.argv[1]
mac_addr = sys.argv[2]
topic = "plug/data/" + mac_addr

client = mqtt.Client()  # Initialize
client.connect(mqttBroker)  # I think this assumes the default port

while True:
    randNumber = uniform(0.0, 100.0)
    message = str(randNumber)
    client.publish(topic, message)
    print(str(topic) + ": " + message)

    # DEBUG
    # print("DEBUG:", client._client_id)
    
    time.sleep(1)
