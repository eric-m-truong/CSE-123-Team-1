import paho.mqtt.client as mqtt
from sys import exit
import logging
from db import connection, util, table_classes


"""
todo:
  - accumulate values in buffer
  - periodically flush to db
  - add MAC to mqtt_datagen
"""

# Parses CSV into a list
csv_to_list = lambda csv_str : list(map(str.strip, csv_str.split(',')))

def run():
  def on_message(client, userdata, message):
    ts, pwr = csv_to_list(message.payload.decode("utf-8"))
    mac_addr = message.topic.split('/').pop()   # Grabs the MAC Address from the MQTT topic
    logging.debug(f'\n ts:  {ts}\n pwr: {pwr}\n mac: {mac_addr}\n')

    con = connection.connect()

    # If this plug doesn't exist in the database, add it
    if not util.get_plug_by_mac(con, mac_addr):
      plug = table_classes.Plug(mac_addr, is_on=True)   # Since the plug sent a message, it should be on
      util.add_plug(con, plug)                          # Add the plug into the database

    # Add the datapoint
    new_datapoint = table_classes.Datapoint(ts, mac_addr, pwr)
    util.add_data(con, new_datapoint)


  # init client
  try:
    client = mqtt.Client("listener")
    client.username_pw_set("user", "pass")  # TODO put the actual username and password here 
    client.connect("mosquitto.projectplux.info")
    logging.info(f"{__name__}: Connected.")
    client.subscribe("plux/data/+")
    client.on_message=on_message
    client.loop_forever()
  except ConnectionRefusedError:
    logging.info(f"No broker running on mosquitto.projectplux.info, exiting...")
    exit(1)


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run()
