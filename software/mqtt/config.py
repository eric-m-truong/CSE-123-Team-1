import json
import sys
from pathlib import Path
from mergedeep import merge, Strategy

CONFIG_PATH = 'config.json'

default = {
    'broker': {
        'ip':   'localhost',
        'user': '',
        'pass': '',
        'port': {
          'mqtt': '1883',
          'websocket': '8883',
        },
        'useSSL': 'false',
     },
    'webserver': {
      'port': '5000'
    }
}


def init():
  assert not Path(CONFIG_PATH).exists()
  with open(CONFIG_PATH, 'w') as cfg:
    json.dump(default, cfg, indent=2)


this = sys.modules[__name__].__dict__
merge(this, default, strategy=Strategy.REPLACE) # ensure always defaults

try:
  with open(CONFIG_PATH) as cfg:
    j = json.load(cfg)
    merge(this, j, strategy=Strategy.REPLACE)
except FileNotFoundError:
  print(f'initialized config with default values at {CONFIG_PATH}',
         'change these values to your own broker')
  init()

print(f'loaded {__name__}')
