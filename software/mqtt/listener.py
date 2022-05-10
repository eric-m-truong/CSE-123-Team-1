import paho.mqtt.client as mqtt
from sys import exit
import logging
from functools import cache

from db import connection, util, table_classes
from mqtt import config


csv_to_list = lambda csv_str : list(map(str.strip, csv_str.split(',')))


def run():
  con = connection.connect() # share among below funcs


  buffer = []  # used by parse_data_message


  @cache
  def add_mac(mac_addr):
    """ add a mac to the db. this function caches args and returns nothing, so
        calling this function twice with the same mac should do nothing. """
    logging.debug(f'querying db for {mac_addr}')
    if not util.get_plug_by_mac(con, mac_addr):
      logging.debug(f'{mac_addr} is new, adding to db')
      plug = table_classes.Plug(mac_addr, is_on=True)   # Sent msg, should be on
      util.add_plug(con, plug)


  def parse_data_message(mac_addr, message):
    ts, pwr = csv_to_list(message.payload.decode("utf-8"))
    # logging.debug(f'\n ts:  {ts}\n pwr: {pwr}\n mac: {mac_addr}\n')

    add_mac(mac_addr)

    # Add the datapoint
    d = table_classes.Datapoint(ts, mac_addr, pwr)
    buffer.append(d)

    if len(buffer) >= 24:
      util.add_data_many(con, buffer)
      buffer.clear()
      logging.debug('flushing plug data to db')


  def parse_ack_message(mac_addr, message):
    """ change db value on ACK. assumes a binary message of 0/1. """
    if util.get_plug_by_mac(con, mac_addr):
      set_status = int(message.payload.replace(b'\x00', b''))
      util.upd_status(con, set_status, mac_addr)
      logging.info(f'updated {mac_addr} to {set_status}')


  def on_message(client, userdata, message):
    topic, mac_addr = message.topic.split('/')[-2:]
    match topic:
      case 'data':
        parse_data_message(mac_addr, message)
      case 'ack':
        parse_ack_message(mac_addr, message)



  # init client
  try:
    client = mqtt.Client()
    client.username_pw_set(config.broker['user'], config.broker['pass'])
    client.connect(config.broker['ip'])

    logging.info(f"connected.")

    channels = ["plux/data/+", "plux/control/ack/+"]
    client.subscribe(list(map(lambda x: (x, 0), channels)))

    client.on_message=on_message
    client.loop_forever()
  except ConnectionRefusedError:
    logging.info(f"No broker running on {config.broker['ip']}, exiting...")
    exit(1)


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run()
