#!/usr/bin/python3

import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

from db.util import *
from db.table_classes import *
from db.query import *
from db.connection import connect
from server.data.db_path import DB_PATH

# Constants
# DATA_DIR = '../data/'
# DB_NAME = 'data.sqlite'
mqttBroker = "broker.hivemq.com"

######################################################
#          MQTT Message Handling (Callback)
######################################################
# Is called whenever the server receives an MQTT message
def on_message(client, userdata, message):
    msg_string = str(message.payload.decode("utf-8"))

    # Parse Message (CSV String to list)
    msg_list = msg_string.split(",")            # Splits message into list
    msg_list = list(map(str.strip, msg_list))   # Strips whitespace

    # Parse MAC Address from topic.
    mac_addr = message.topic.split('/').pop()   # Grabs the last element
    
    connection = connect()
    
    # If this plug doesn't exist in the database, add it
    if not get_plug_by_mac(connection, mac_addr).fetchall():   # If returns an empty list
        add_plug(connection, Plug(mac_addr, True))  # Add a plug into the database

    # Add the datapoint
    new_datapoint = Datapoint(str(datetime.now()), mac_addr, msg_list[0])
    add_data(connection, new_datapoint)

    connection.commit()
    connection.close()

    # DEBUG
    print(new_datapoint)




######################################################
#                       MAIN
######################################################

#-------------
# INITIALIZE
#-------------

# SQLite
connection = connect()
connection.commit()
connection.close()

# MQTT
client = mqtt.Client("Server")
client.connect(mqttBroker)
client.loop_start()  # Runs a loop in a background thread
client.subscribe("plux/data/#")
client.on_message=on_message

#--------------------------
# Close Server on Command
#--------------------------
running = True
while (running):
    command = input("Type 'stop' to close the server\n\n")
    running = ("stop" != command)
    
# Graceful Close
client.loop_stop()  # MQTT
#TODO Maybe change this to the blocking version since
#TODO we don't need to do any graceful closing.




######################################################
#                   DEBUG ZONE
######################################################
# new_plug = Plug("prototype")
# db_add_plug(cursor, new_plug)
# connection.commit()


# cursor.execute("SELECT * FROM Plugs WHERE name=(:name)", {'name': new_plug.name})
# print(cursor.fetchall())

# # Testing Datapoints
# example_plug_id = 1
# db_add_data(cursor, Datapoint(datetime.now(), example_plug_id, 420.69))
# cursor.execute("SELECT * from Data WHERE plug_id=(:plug_id)", {'plug_id': example_plug_id})
# print(cursor.fetchall())

# connection.commit()

# connection.close()  # Good practice to close
