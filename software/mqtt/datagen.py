import paho.mqtt.client as mqtt
from random import random, randrange
from time import sleep, time
from sys import exit
import logging


def run(plug_num):
  """
  Randomly generates data and publishes to a random plug channel
  Send a plug number to channel "ctrl" to toggle the plug ON/OFF
  """
  print(plug_num)

  try:
    client = mqtt.Client("datagen")
    client.connect("localhost")
  except ConnectionRefusedError:
    logging.info(f"No broker running on localhost, exiting...")
    exit(1)
  logging.info(f"{__name__}: Connected.")

  ENABLED = 1
  DISABLED = 0

  status = [ENABLED for i in range(plug_num)]


  def on_message(client, userdata, message):
    plug_num = int(message.payload)
    status[plug_num] = not status[plug_num]
    logging.debug(f'tog {plug_num} to {status[plug_num]}')


  client.subscribe("ctrl")
  client.on_message=on_message
  client.loop_start()

  while True:
    if status[(rnd_plug_num := randrange(plug_num))] == ENABLED:
      topic = f"plug/{rnd_plug_num}"
      message = f"{time()},{random()}"
      client.publish(topic, message)
      sleep(random())


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run(4)
