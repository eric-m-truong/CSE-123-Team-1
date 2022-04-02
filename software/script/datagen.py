import paho.mqtt.client as mqtt
from random import random, randrange
from time import sleep, time
from sys import argv, exit

"""
Randomly generates data and publishes to a random plug channel
Pass # of plugs to simulate. No arg = 1 plug.
"""

try:
  client = mqtt.Client("datagen")
  client.connect("localhost")
except ConnectionRefusedError:
  print(f"{argv[0]}: No broker running on localhost, exiting...")
  exit(1)

plugs = int(argv[1] if len(argv) == 2 else 1)

if plugs <= 0:
  print(f"{argv[0]}: Specify at least 1 plug")
  exit(1)

while True:
  topic = f"plug/{randrange(plugs)}"
  message = f"{time()},{random()}"
  client.publish(topic, message)
  sleep(random())
