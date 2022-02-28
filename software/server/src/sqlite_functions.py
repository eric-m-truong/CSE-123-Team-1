import sqlite3
from table_classes import Plug, Datapoint

def db_init(cursor):
    # # Users
    # try:
    #     cursor.execute(
    #         """CREATE TABLE Users (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             name VARCHAR(255) NOT NULL
    #         )"""
    #     )
    # except:
    #     print("Users table may already exist")

    # # Hubs
    # try:
    #     cursor.execute(
    #         """CREATE TABLE Hubs (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             user_id INTEGER,
    #             FOREIGN KEY(user_id) REFERENCES Users(id)
    #         )"""
    #     )
    # except:
    #     print("Hubs table may already exist")

    # Plugs
    try:
        cursor.execute( #TODO Add the FOREIGN KEY hub_id back in
            """
            CREATE TABLE Plugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
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
                plug_id INTEGER,
                power FLOAT,
                FOREIGN KEY(plug_id) REFERENCES Plugs(id)
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
    cursor.execute("""INSERT INTO Plugs VALUES (:id, :name)""", {'id': None, 'name': plug.name})
    # cursor.execute("""INSERT INTO Plugs VALUES (?)""", (plug.name))

def db_add_data(cursor, datapoint):
    cursor.execute("""INSERT INTO Data VALUES (:timestamp, :plug_id, :power)""", {'timestamp': datapoint.timestamp, 'plug_id': datapoint.plug_id, 'power': datapoint.power})
