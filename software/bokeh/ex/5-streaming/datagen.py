import paho.mqtt.client as mqtt
from random import random
from time import sleep, time

topic = "plug/0"

client = mqtt.Client("datagen")
client.connect("localhost")

while True:
    message = f"{time()},{random()}"
    client.publish(topic, message)
    # print(topic, ":", message)
    sleep(random())
