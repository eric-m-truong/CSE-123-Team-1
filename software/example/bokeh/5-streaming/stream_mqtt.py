import numpy as np
from bokeh.plotting import curdoc, figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
import paho.mqtt.client as mqtt


pwr_queue = []
ts_queue = []
cds = ColumnDataSource(data={'x': [], 'y': []})

def on_message(client, userdata, message):
  ts, pwr = map(float, message.payload.split(b','))
  ts_queue.append(ts)
  pwr_queue.append(pwr)


def stream():
  global ts_queue, pwr_queue
  # append any new data to the graph
  cds.stream({'x': ts_queue, 'y': pwr_queue})
  # then clear the queues
  pwr_queue.clear()
  ts_queue.clear()


# init plot
p = figure(sizing_mode='stretch_width')
p.line('x', 'y', source=cds)
curdoc().add_root(column(p))

# init client
client = mqtt.Client("stream")
client.connect("localhost")
client.subscribe("plug/0")
client.on_message=on_message

# loop
client.loop_start()  # Runs a loop in a background thread
curdoc().add_periodic_callback(stream, 100)
