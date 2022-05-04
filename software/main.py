import logging
import argparse
from importlib import import_module

from db.connection import DB_PATH
from script.dispatcher import exec, execfn
from script import dispatcher
from mqtt import listener, config # read config now so forks won't read again
from server import handler

parser = argparse.ArgumentParser(description='Run plux server.')
parser.add_argument('--provision', '-p',
                    action=argparse.BooleanOptionalAction,
                    default=False,
                    help='Provision the database with random data from '
                         'yesterday to today.')
parser.add_argument('--dummy', '-d',
                    action=argparse.BooleanOptionalAction,
                    default=False,
                    help='Generate dummy plug data.')
parser.add_argument('--broker', '-b',
                    action=argparse.BooleanOptionalAction,
                    default=False,
                    help='Run a local broker.')
args = parser.parse_args()

format = '%(levelname)s:%(module)s:%(message)s'
logging.basicConfig(format=format, level=logging.DEBUG)


if args.provision:
  PLUG_NUM = 4
  import_module('db.datagen').generate(PLUG_NUM)

# order matters here unfortunately. flask must come last so it isn't the
# processt the dispatcher waits for. if it is, it will eat one of our
# KeyboardInterrupt signals.
es = [lambda: execfn(listener.run),
      lambda: execfn(handler.app.run,
        host='0.0.0.0', # listen on all addresses: accessible outside localhost
        port=config.webserver['port'],
        debug=False # don't show python errors in browser on error
        )
     ]

if args.broker:
  import inspect

  ports = config.broker['port']
  mqtt_port, ws_port = ports['mqtt'], ports['websocket']
  mosquitto_conf = f"""listener {mqtt_port}
                       protocol mqtt

                       listener {ws_port}
                       protocol websockets

                       allow_anonymous true"""
  mosquitto_conf_clean = inspect.cleandoc(mosquitto_conf) # remove indent
  print(mosquitto_conf_clean)
  with open('mosquitto.conf', 'w') as f:
    f.write(mosquitto_conf_clean)

  es.insert(0, lambda: exec('mosquitto', ['-c',  'mosquitto.conf']))

if args.dummy:
  es.insert(1, lambda: execfn(import_module('mqtt.datagen').run))

try:
  dispatcher.run(es)
except KeyboardInterrupt:
  pass
