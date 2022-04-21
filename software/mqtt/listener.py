import paho.mqtt.client as mqtt
from sys import exit
import logging
from db import connection, util, table_classes
from mqtt import config


csv_to_list = lambda csv_str : list(map(str.strip, csv_str.split(',')))


def run():
  buffer = []

  def on_message(client, userdata, message):
    ts, pwr = csv_to_list(message.payload.decode("utf-8"))
    mac_addr = message.topic.split('/')[-1]   # Grabs the MAC Address from the MQTT topic
    logging.debug(f'\n ts:  {ts}\n pwr: {pwr}\n mac: {mac_addr}\n')

    con = connection.connect() # Move outside fn?

    # TODO: may benefit from caching existence checks
    # If this plug doesn't exist in the database, add it
    if not util.get_plug_by_mac(con, mac_addr):
      plug = table_classes.Plug(mac_addr, is_on=True)   # Since the plug sent a message, it should be on
      util.add_plug(con, plug)                          # Add the plug into the database

    # Add the datapoint
    d = table_classes.Datapoint(ts, mac_addr, pwr)
    buffer.append(d)

    if len(buffer) >= 24:
      util.add_data_many(con, buffer)
      buffer.clear()
      logging.debug('flushing plug data to db')
    else:
      logging.debug(len(buffer))


  # init client
  try:
    client = mqtt.Client()
    client.username_pw_set(config.broker['user'], config.broker['pass'])
    client.connect(config.broker['ip'])
    logging.info(f"{__name__}: Connected.")
    client.subscribe("plux/data/+")
    client.on_message=on_message
    client.loop_forever()
  except ConnectionRefusedError:
    logging.info(f"No broker running on {config.broker['ip']}, exiting...")
    exit(1)


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run()
