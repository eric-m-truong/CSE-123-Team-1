import sqlite3
from pathlib import Path

from db import query


DB_PATH = f'{Path.cwd()}/data.sqlite'


def connect():
  """
  Connects to the db. If the db path does not exist, initializes db and adds
  Plugs and Data table.
  Invariant: after running this function, Plugs and Data table will exist in db.
  Returns: sqlite3.Connection
  """
  con = sqlite3.connect(DB_PATH)
  try:
    init(con) # fails if already exists
  except sqlite3.OperationalError:
    pass
  return con


def execute(con, query, *parm):
  """
  Executes a query, automatically committing any changes to the db.
  Returns: sqlite3.Cursor


  USAGE NOTES

  An arbitrary number of parameters may be passed to execute. If a dict is
  passed as the 1st value, it will be the only value passed to
  sqlite3.execute() and will be treated as named parameters in the sqlite
  query.

  The query string can make use of the dict by referring to any value
  by :key_value. All other arguments will be passed in a tuple and can be
  referred in the query string with %.


  EXAMPLES

  parm = {'timestamp': ..., 'plug_id': ..., 'power': ...}
  query = "INSERT INTO Data VALUES (:timestamp, :plug_id, :power)"
  execute(con, query, parm)

  Keys in parm[0] will be substituted in the query string by name.

  mac = "..."
  query = "SELECT * FROM Plugs WHERE mac_addr=(?)"
  execute(con, query, parm)

  The value for the mac adress will be substituted where ? appears in the
  query.
  NOTE: paranthesis not required around ?

  This function always returns a Cursor object to save computation. To fetch
  the rows for a query (if needed), treat the return value as an iterator or
  call .fetch{one,all} on it.
  """
  with con: # auto calls .commit()
    p = parm[0] if len(parm) == 1 and isinstance(parm[0], dict) else parm
    return con.execute(query, p)


def executemany(con, query, parm):
  with con: # auto calls .commit()
    return con.executemany(query, parm)


def init(con):
  """ Creates Plugs and Data table. See db.query for the query strings. """
  execute(con, query.INIT_PLUG)
  execute(con, query.INIT_DATA)
