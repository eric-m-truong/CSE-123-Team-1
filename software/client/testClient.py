# Code taken and adapted from:
# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "128.114.62.135"

client = mqtt.Client("laptop")  # Idk what this line does
client.connect(mqttBroker)  # I think this assumes the default port

while True:
    topic = "plug/laptop"
    randNumber = uniform(20.0, 21.0)
    message = "Now o' clock, Laptop, " + str(randNumber) + "\n"
    client.publish(topic, message)
    print("Just published to topic " + topic + "\n" + message)
    time.sleep(1)
