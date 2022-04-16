import paho.mqtt.client as mqtt
from sys import exit
import logging
import json


"""
todo:
  - accumulate values in buffer
  - periodically flush to db
  - add MAC to mqtt_datagen
"""


def run():
  def on_message(client, userdata, message):
    payload = json.loads(message.payload)     # Converts the JSON string to a python dictionary
    mac_addr = message.topic.split('/').pop() # Grabs the MAC Address from the MQTT topic
    logging.debug(f'\n ts:  {payload["timestamp"]}\n pwr: {payload["power"]}\n mac: {mac_addr}\n')


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
