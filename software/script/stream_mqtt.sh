#!/bin/bash

if [ "$#" -lt 2 ]; then
  name=$(basename "$0")
  echo "run a local mqtt and generate data on a channel"
  echo "usage: $name num_plugs [args...]"
  exit 1
fi

if ! [ -x "$(command -v mosquitto)" ]; then
  echo 'Mosquitto not installed, aborting' >&2
  exit 1
fi

if [ -z "$(pip list | grep -i "paho-mqtt")" ]; then
  echo 'python-paho-mqtt not installed, aborting' >&2
  exit 1
fi

plug_num=$1
shift

trap 'kill $(jobs -p)' EXIT

(cd $(dirname $0) && mosquitto -c mosquitto.conf) &
(cd $(dirname $0) && python mqtt_datagen.py $plug_num) &
$@ &

wait
