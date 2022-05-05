import sqlite3
from random import random, randint, choice
from datetime import datetime, timedelta

from pandas import date_range

from db import util, table_classes
from db.connection import connect


"""
Create a database file "data.sqlite", populate Plugs table with plug_num plugs
and a random MAC, then populate Data table with random data using the MAC of any
of the plugs and a power reading in range (0,1)
"""

def generate(plug_num):
  DATA_MAX_NUM = 30
  DATE_OFFSET = timedelta(days=-1)

  gen_MAC = lambda: ':'.join([f'{randint(0x0, 0xFFFF):04X}' for i in range(4)])
  MACS = [gen_MAC() for i in range(plug_num)]

  con = connect()

  for MAC in MACS:
    plug = table_classes.Plug(MAC, True)
    util.add_plug(con, plug)

  NUM_PTS = randint(DATA_MAX_NUM//2,DATA_MAX_NUM)

  dates = date_range(start = datetime.now() + DATE_OFFSET,
                     end = datetime.now(),
                     periods = NUM_PTS)

  for MAC in MACS:
    print('generating data for', MAC)
    for i in range(NUM_PTS):
      # MAC = choice(MACS)
      pwr = NUM_PTS - i
      ts = dates[i].timestamp()
      dp = table_classes.Datapoint(ts, MAC, pwr)
      print(dp)
      util.add_data(con, dp)

  con.close()


if __name__ == '__main__':
  generate(4)
