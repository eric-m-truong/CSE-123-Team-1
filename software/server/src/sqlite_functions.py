import sqlite3
from plug import Plug

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
    #     print("Users table already exists")

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
    #     print("Hubs table already exists")

    # Plugs
    try:
        cursor.execute( #TODO Add the FOREIGN KEY hub_id back in
            """CREATE TABLE Plugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
            )"""
        )
    except:
        print("Plugs table already exists")

    # Data
    try:
        cursor.execute(
            """CREATE TABLE Data (
                timestamp DATETIME,
                plug_id INTEGER,
                power FLOAT,
                FOREIGN KEY(plug_id) REFERENCES Plugs(id)
            )"""
        )
    except:
        print("Data table already exists")

def db_add_plug(cursor, plug):
    cursor.execute("""INSERT INTO Plugs VALUES (:id, :name)""", {'id': None, 'name': plug.name})
    # cursor.execute("""INSERT INTO Plugs VALUES (?)""", (plug.name))

