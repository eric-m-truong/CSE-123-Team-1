import logging
import argparse
from importlib import import_module

from db.connection import DB_PATH
from script.dispatcher import exec, execfn
from script import dispatcher
from mqtt import listener, config # read config now so forks won't read again


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
parser.add_argument('--webserver', '-w',
                    action=argparse.BooleanOptionalAction,
                    default=False,
                    help='Run a local flask server.')
args = parser.parse_args()

format = '%(levelname)s:%(module)s:%(message)s'
logging.basicConfig(format=format, level=logging.DEBUG)


if args.provision:
  PLUG_NUM = 4
  import_module('db.datagen').generate(PLUG_NUM)

# order matters here unfortunately. flask must come last so it isn't the
# processt the dispatcher waits for. if it is, it will eat one of our
# KeyboardInterrupt signals.
es = [lambda: execfn(listener.run)]

if args.broker:
  import inspect
  import tempfile

  ports = config.broker['port']
  mqtt_port, ws_port = ports['mqtt'], ports['websocket']
  mosquitto_conf = f"""listener {mqtt_port}
                       protocol mqtt

                       listener {ws_port}
                       protocol websockets

                       allow_anonymous true"""
  mosquitto_conf_clean = inspect.cleandoc(mosquitto_conf) # remove indent

  # generate a temp mosquitto config from mqtt.config values
  # we do this b/c mosquitto is poorly written and cannot accept a config from
  # stdin nor the file /dev/stdin (how'd they manage to mess that one up?)
  f = tempfile.NamedTemporaryFile(mode='w', delete=False)
  f.write(mosquitto_conf_clean)
  f.close() # close before letting mosquitto incorrectly open the file


  def run_local_mosquitto():
    """ fork mosquitto, register atexit to rm tmp config, then wait (block)
    on it. parent will exit when child exits, and rm tmp file. """
    import atexit
    from os import getpid, waitpid

    pid = exec('mosquitto', ['-c', f.name])
    atexit.register(lambda: import_module('pathlib').Path(f.name).unlink())
    waitpid(pid, 0)


  es.append(lambda: execfn(run_local_mosquitto))

if args.dummy:
  es.append(lambda: execfn(import_module('mqtt.datagen').run))

if args.webserver:
  from server import handler

  es.append(
    lambda: execfn(handler.app.run,
      host='0.0.0.0', # listen on all addresses: accessible outside localhost
      port=config.webserver['port'],
      debug=False # don't show python errors in browser on error
      )
    )

try:
  dispatcher.run(es)
except KeyboardInterrupt:
  pass
