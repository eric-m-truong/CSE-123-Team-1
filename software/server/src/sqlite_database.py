import sqlite3
from sqlite_functions import *

DATA_DIR = '../data/'
DB_NAME = 'data.sqlite'

# connection = sqlite3.connect(DATA_DIR + DB_NAME)
connection = sqlite3.connect(":memory:") # DEBUG
cursor = connection.cursor()

db_init(cursor)
new_plug = Plug("prototype")
db_add_plug(cursor, new_plug)
connection.commit()


cursor.execute("SELECT * FROM Plugs WHERE name=(:name)", {'name': new_plug.name})
print(cursor.fetchall())


connection.commit()

connection.close()  # Good practice to close