#!/bin/bash

if ! [ -x "$(command -v mosquitto)" ]; then
  echo 'Mosquitto not installed, aborting' >&2
  exit 1
fi

if ! [ -x "$(command -v bokeh)" ]; then
  echo 'bokeh not installed, aborting' >&2
  exit 1
fi

if [ -z "$(pip list | grep -i "paho-mqtt")" ]; then
  echo 'python-paho-mqtt not installed, aborting' >&2
  exit 1
fi

mosquitto &
python datagen.py &
bokeh serve --show stream_mqtt.py
