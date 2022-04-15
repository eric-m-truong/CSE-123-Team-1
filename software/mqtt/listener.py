import paho.mqtt.client as mqtt
from sys import exit
import logging


"""
todo:
  - accumulate values in buffer
  - periodically flush to db
  - add MAC to mqtt_datagen
"""


def run():
  def on_message(client, userdata, message):
    ts, pwr = map(float, message.payload.split(b','))
    logging.debug(f'ts: {ts} pwr: {pwr}')


  # init client
  try:
    client = mqtt.Client("listener")
    client.connect("localhost")
    logging.info(f"{__name__}: Connected.")
    client.subscribe("plug/+")
    client.on_message=on_message
    client.loop_forever()
  except ConnectionRefusedError:
    logging.info(f"No broker running on localhost, exiting...")
    exit(1)


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  run()
