import sqlite3
from pathlib import Path

from db import query

from server.data.db_path import *

def connect():
  con = sqlite3.connect(DB_PATH)
  try:
    init(con) # fails if already exists
  except sqlite3.OperationalError:
    pass
  return con


def execute(con, query, *parm):
  with con: # auto calls .commit()
    p = parm[0] if len(parm) == 1 and isinstance(parm[0], dict) else parm
    return con.execute(query, p)


def init(con):
  execute(con, query.INIT_PLUG)
  execute(con, query.INIT_DATA)
