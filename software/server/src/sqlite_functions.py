import sqlite3
from table_classes import Plug, Datapoint

def db_init(cursor):

    # Plugs
    try:
        cursor.execute( #TODO Add the FOREIGN KEY hub_id back in
            """
            CREATE TABLE Plugs (
                mac_addr TEXT PRIMARY KEY,
                alias TEXT,
                is_on BOOLEAN NOT NULL
            )
            """
        )
    except:
        print("Plugs table may already exist")

    # Data
    try:
        cursor.execute(
            """
            CREATE TABLE Data (
                timestamp DATETIME,
                plug_id TEXT,
                power FLOAT,
                FOREIGN KEY(plug_id) REFERENCES Plugs(mac_addr)
            )
            """
        )
    except:
        print("Data table may already exist")

    # Indexes (for speeding up searches)
    try:
        cursor.execute(
            """
            CREATE INDEX timestamp_index
            ON Data(timestamp)
            """
        )
        cursor.execute(
            """
            CREATE INDEX plug_id_index
            ON Data(plug_id)
            """
        )
    except:
        print("Index may already exist")

def db_add_plug(cursor, plug):
    cursor.execute("""INSERT INTO Plugs VALUES (:mac_addr, :alias, :is_on)""", {'mac_addr': plug.mac_addr, 'name': plug.alias, 'is_on': plug.is_on})

def db_add_data(cursor, datapoint):
    cursor.execute("""INSERT INTO Data VALUES (:timestamp, :plug_id, :power)""", {'timestamp': datapoint.timestamp, 'plug_id': datapoint.plug_id, 'power': datapoint.power})
