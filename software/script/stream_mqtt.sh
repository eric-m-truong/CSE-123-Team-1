#!/bin/bash

if [ "$#" -eq 0 ]; then
  name=$(basename "$0")
  echo "run a local mqtt and generate data on a channel"
  echo "usage: $name script.py"
  exit 1
fi


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


trap 'kill $(jobs -p)' EXIT

mosquitto &
python ../../bokeh/ex/5-streaming/datagen.py &
python $1 &

wait
