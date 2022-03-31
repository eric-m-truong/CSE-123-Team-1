# Reference:
# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

import paho.mqtt.client as mqtt
import datetime
import time

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Server")
client.connect(mqttBroker)

client.loop_start()  # Runs a loop in a background thread

client.subscribe("plug/#")
client.on_message=on_message

# Go forever until stopped
running = True
while (running):
    command = input("Type 'stop' to close the server\n")
    running = ("stop" != command)

client.loop_stop()