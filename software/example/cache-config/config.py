import json
import sys
from pathlib import Path


CONFIG_PATH = 'config.json'


def init():
  assert not Path(CONFIG_PATH).exists()
  default = {
      'broker': {
          'ip':   'address',
          'user': 'name',
          'pass': 'word',
       },
  }
  with open(CONFIG_PATH, 'w') as cfg:
    json.dump(default, cfg, indent=2)


this = sys.modules[__name__].__dict__

try:
  with open(CONFIG_PATH) as cfg:
    j = json.load(cfg)
    this.update(j)
except FileNotFoundError:
  print(f'initialized config with default values at {CONFIG_PATH}',
         'change these values to your own broker')
  init()

print(f'loaded {__name__}')
