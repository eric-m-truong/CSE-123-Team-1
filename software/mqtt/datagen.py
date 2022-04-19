import paho.mqtt.client as mqtt
from random import random, randrange
from time import sleep, time
from sys import exit
import logging
from mqtt import config


def run(plug_num):
  """
  Randomly generates data and publishes to a random plug channel
  Send a plug number to channel "ctrl" to toggle the plug ON/OFF
  """
  print(plug_num)

  try:
    client = mqtt.Client("datagen") # may need to randomize name
    client.username_pw_set(config.broker['user'], config.broker['pass'])
    client.connect(config.broker['ip'])
  except ConnectionRefusedError:
    logging.info(f"No broker running on {config.broker['ip']}, exiting...")
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
      topic = f"plux/data/{rnd_plug_num}"
      message = f"{time()},{random()}"
      # logging.debug(f'{topic}: {message}')
      client.publish(topic, message)
      sleep(random())


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run(4)
