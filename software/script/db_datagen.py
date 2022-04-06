import sqlite3
from random import random, randint, choice
from datetime import datetime

# import sys
# sys.path.append('..') # needed for db

from db import util, table_classes
from db.connection import connect

"""
Create a database file "data.sqlite", populate Plugs table with PLUG_NUM plugs
and a random MAC, then populate Data table with random data using the MAC of any
of the plugs and a power reading in range (0,1)
"""

DATA_MAX_NUM = 30
gen_MAC = lambda: ':'.join([f'{randint(0x0, 0xFFFF):04X}' for i in range(4)])
PLUG_NUM = 4
MACS = [gen_MAC() for i in range(PLUG_NUM)]

con = connect()

for MAC in MACS:
  plug = table_classes.Plug(MAC, True)
  util.add_plug(con, plug)

for i in range(randint(DATA_MAX_NUM//2,DATA_MAX_NUM)):
  MAC = choice(MACS)
  pwr = random()
  ts = str(datetime.now())
  dp = table_classes.Datapoint(ts, MAC, pwr)
  util.add_data(con, dp)

con.close()
