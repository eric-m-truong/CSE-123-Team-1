import sqlite3
from sqlite_functions import *
from datetime import datetime
import paho.mqtt.client as mqtt

######################################################
#          MQTT Message Handling (Callback)
######################################################
def on_message(client, userdata, message):
    msg_string = str(message.payload.decode("utf-8"))
    # print("Received message: ", msg_string)   # DEBUG

    # Parse Message (CSV String to list)
    msg_list = msg_string.split(",")            # Splits message into list
    msg_list = list(map(str.strip, msg_list))   # Strips whitespace
    
    ##DEBUG
    print(msg_list)





######################################################
#                   INITIALIZE
######################################################
# Constants
DATA_DIR = '../data/'
DB_NAME = 'data.sqlite'
mqttBroker = "broker.hivemq.com"

# SQLite
# connection = sqlite3.connect(DATA_DIR + DB_NAME)  #TODO Uncomment to use an actual database
connection = sqlite3.connect(":memory:")            #TODO Remove this DEBUG line
cursor = connection.cursor()
db_init(cursor)

# MQTT
client = mqtt.Client("Server")
client.connect(mqttBroker)
client.loop_start()  # Runs a loop in a background thread
client.subscribe("plug/#")
client.on_message=on_message


######################################################
#             Close Server on Command
######################################################
# Closing Command
running = True
while (running):
    command = input("Type 'stop' to close the server\n\n")
    running = ("stop" != command)
    
# Graceful Close
client.loop_stop()  # MQTT
connection.commit() # SQLite
connection.close()  # SQLite





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