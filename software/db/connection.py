import sqlite3
from pathlib import Path

from . import query


DATA_DIR = '../data/'
DB_NAME = 'data.sqlite'
DB_PATH = DATA_DIR + DB_NAME

# connect = lambda: sqlite3.connect(DB_NAME)


def connect():
  con = sqlite3.connect(DB_NAME)
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
