import numpy as np
from bokeh.plotting import curdoc, figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
import paho.mqtt.client as mqtt


cds = ColumnDataSource(data={'x': [], 'y': []})
curdoc = curdoc() # need to store a ref to get updates to work in on_message


def on_message(client, userdata, message):
  ts, pwr = map(float, message.payload.split(b','))
  print(ts, pwr)
  curdoc.add_next_tick_callback(lambda: cds.stream({'x': [ts], 'y': [pwr]}))


# init plot
p = figure(sizing_mode='stretch_width')
p.line('x', 'y', source=cds)
curdoc.add_root(column(p))

# init client
client = mqtt.Client("stream")
client.connect("localhost")
client.subscribe("plug/0")
client.on_message=on_message

# loop
client.loop_start()
