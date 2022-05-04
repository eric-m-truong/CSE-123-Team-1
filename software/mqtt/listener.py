import paho.mqtt.client as mqtt
from sys import exit
import logging
from db import connection, util, table_classes
from mqtt import config


csv_to_list = lambda csv_str : list(map(str.strip, csv_str.split(',')))


def run():
  con = connection.connect() # share among below funcs


  buffer = []  # used by parse_data_message

  def parse_data_message(mac_addr, message):
    ts, pwr = csv_to_list(message.payload.decode("utf-8"))
    # logging.debug(f'\n ts:  {ts}\n pwr: {pwr}\n mac: {mac_addr}\n')

    # TODO: may benefit from caching existence checks
    # If this plug doesn't exist in the database, add it
    if not util.get_plug_by_mac(con, mac_addr):
      plug = table_classes.Plug(mac_addr, is_on=True)   # Sent msg, should be on
      util.add_plug(con, plug)

    # Add the datapoint
    d = table_classes.Datapoint(ts, mac_addr, pwr)
    buffer.append(d)

    if len(buffer) >= 24:
      util.add_data_many(con, buffer)
      buffer.clear()
      logging.debug('flushing plug data to db')


  def parse_ack_message(mac_addr, message):
    """ change db value on ACK. assumes a binary message of 0/1. """
    assert util.get_plug_by_mac(con, mac_addr)
    set_status = int(message.payload)
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

    channels = ["plux/data/+", "plux/ctrl/ack/+"]
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
