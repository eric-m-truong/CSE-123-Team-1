#!/usr/bin/python3

from pathlib import Path
import logging

from db.connection import DB_PATH
import db.datagen as dbgen
import mqtt.datagen as mqttgen
from script.dispatcher import exec, execfn
from script import dispatcher
from mqtt import listener


format = '%(levelname)s:%(module)s:%(message)s'
logging.basicConfig(format=format, level=logging.DEBUG)


"""
1. Delete db
2. Init db w/ db/datagen.py
3. Start mosquitto
4. Start mqtt/datagen.py
5. Start mqtt listener
6. Start flask web server
"""

PLUG_NUM = 4

# Path(DB_PATH).unlink(missing_ok=True)
dbgen.generate(PLUG_NUM)

es = [lambda: execfn(mqttgen.run),
      lambda: execfn(listener.run),
      lambda: exec('flask', ['run'], env={'FLASK_APP': 'server/handler'})
     ]

try:
  dispatcher.run(es)
except KeyboardInterrupt:
  pass
