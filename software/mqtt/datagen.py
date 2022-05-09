import paho.mqtt.client as mqtt
from random import random, randrange
from time import sleep, time
from sys import exit
import logging
from importlib import import_module

import db.connection as dbcon
from mqtt import config


def run():
  """
  Randomly generates data and publishes to a random plug channel
  Send a plug number to channel "control" to toggle the plug ON/OFF
  """
  try:
    client = mqtt.Client() # may need to randomize name
    client.username_pw_set(config.broker['user'], config.broker['pass'])
    client.connect(config.broker['ip'])
  except ConnectionRefusedError:
    logging.info(f"No broker running on {config.broker['ip']}, exiting...")
    exit(1)
  logging.info("Connected.")

  con = dbcon.connect()

  # use a generator to only fetch each value as accessed. better than
  # constructing a whole list to make two lists from its elements.
  names_and_status = ((mac, status)
      for mac, alias, status in dbcon.execute(con, "SELECT * FROM Plugs"))
  try:
    names, status = map(list, zip(*names_and_status)) # inverse zip
  except ValueError:
    logging.warning("no plugs in database. populating...")
    PLUG_NUM = 4
    import_module('db.datagen').generate(PLUG_NUM)
    logging.warning("db populated. exiting...")
    exit(1)

  con.close()


  def on_message(client, userdata, message):
    mac_addr = message.topic.split('/')[-1]
    set_status = int(message.payload)
    plug_num = names.index(mac_addr)
    status[plug_num] = set_status

    sleep(random()) # intro random delay to simulate processing time
    client.publish(f"plux/control/ack/{mac_addr}", set_status)

    logging.debug(f'set {mac_addr} to {status[plug_num]}')


  client.subscribe("plux/control/+")
  client.on_message=on_message
  client.loop_start()

  num_plugs = len(names)

  while True:
    if status[(rnd_plug_num := randrange(num_plugs))]:
      topic = f"plux/data/{names[rnd_plug_num]}"
      message = f"{time()},{random()}"
      # logging.debug(f'{topic}: {message}')
      client.publish(topic, message)
      sleep(random())


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run()
