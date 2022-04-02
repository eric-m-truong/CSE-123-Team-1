#!/bin/bash

if [ "$#" -eq 0 ]; then
  name=$(basename "$0")
  echo "run a local mqtt and generate data on a channel"
  echo "usage: $name [# plugs] script.py [args...]"
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

if [ "$#" -gt 1 ]; then
  plug_num=$1
  shift
else
  plug_num=0
fi

trap 'kill $(jobs -p)' EXIT

mosquitto &
python datagen.py $plug_num &
python $@ &

wait
