import paho.mqtt.client as mqtt
from random import random, randrange
from time import sleep, time
from sys import argv, exit

"""
Randomly generates data and publishes to a random plug channel
Pass # of plugs to simulate. No arg = 1 plug.
Send a plug number to channel "ctrl" to toggle the plug ON/OFF
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

ENABLED = 1
DISABLED = 0

status = [ENABLED for i in range(plugs)]


def on_message(client, userdata, message):
  plug_num = int(message.payload)
  status[plug_num] = not status[plug_num]
  print(f'tog {plug_num} to {status[plug_num]}')


client.subscribe("ctrl")
client.on_message=on_message
client.loop_start()

while True:
  if status[(plug_num := randrange(plugs))] == ENABLED:
    topic = f"plug/{plug_num}"
    message = f"{time()},{random()}"
    client.publish(topic, message)
    sleep(random())
