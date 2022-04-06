from threading import Thread

from flask import Flask, render_template
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme

import numpy as np
from bokeh.models import ColumnDataSource

import paho.mqtt.client as mqtt


app = Flask(__name__)


def bkapp(doc):
  pwr_queue = []
  ts_queue = []


  def on_message(client, userdata, message):
    ts, pwr = map(float, message.payload.split(b','))
    ts_queue.append(ts)
    pwr_queue.append(pwr)


  cds = ColumnDataSource(data={'x': [], 'y': []})


  def callback():
    nonlocal ts_queue, pwr_queue
    # append any new data to the graph
    cds.stream({'x': ts_queue, 'y': pwr_queue})
    # then clear the queues
    pwr_queue.clear()
    ts_queue.clear()


  p = figure(sizing_mode='stretch_width', title='MQTT streaming example')

  random255 = lambda: np.random.randint(255)
  color = tuple(random255() for _ in range(3))
  p.line('x', 'y', source=cds, color=color)

  doc.add_root(column(p))

  # init client
  client = mqtt.Client("stream")
  client.connect("localhost")
  client.subscribe("plug/0")
  client.on_message=on_message

  # loop
  client.loop_start()  # Runs a loop in a background thread
  doc.add_periodic_callback(callback, 100)


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://127.0.0.1:5006/bkapp')
    return render_template("mqtt.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration.
    server = Server({'/bkapp': bkapp},
                    io_loop=IOLoop(),
                    allow_websocket_origin=["127.0.0.1:8000"])
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()

if __name__ == '__main__':
    app.run(port=8000)
