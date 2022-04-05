import sqlite3
from random import random, randint, choice
from sqlite_functions import db_init, db_add_data, db_add_plug
import table_classes
from datetime import datetime

"""
Create a database file "data.sqlite", populate Plugs table with PLUG_NUM plugs
and a random MAC, then populate Data table with random data using the MAC of any
of the plugs and a power reading in range (0,1)
"""

DATA_DIR = '../data/'
DB_NAME = 'data.sqlite'
DATA_MAX_NUM = 30
gen_MAC = lambda: ':'.join([f'{randint(0x0, 0xFFFF):04X}' for i in range(4)])
PLUG_NUM = 4
MACS = [gen_MAC() for i in range(PLUG_NUM)]

connection = sqlite3.connect(DATA_DIR + DB_NAME)
cursor = connection.cursor()
db_init(cursor)

for MAC in MACS:
  plug = table_classes.Plug(MAC, True)
  db_add_plug(cursor, plug)

for i in range(randint(DATA_MAX_NUM//2,DATA_MAX_NUM)):
  MAC = choice(MACS)
  pwr = random()
  ts = str(datetime.now())
  dp = table_classes.Datapoint(ts, MAC, pwr)
  db_add_data(cursor, dp)

connection.commit() # finalize additions
connection.close()
