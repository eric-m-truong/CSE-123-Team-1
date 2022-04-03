from threading import Thread
from collections import defaultdict
from functools import cache

from flask import Flask, render_template, request
from tornado.ioloop import IOLoop

from bokeh.embed import server_document, server_session
from bokeh.util.token import generate_session_id
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.client import pull_session

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

  # watch a particular channel
  args = doc.session_context.request.arguments
  plug_num = int(args.get('plug')[0]) if 'plug' in args else 0

  # init client
  # https://stackoverflow.com/a/40750674
  client = mqtt.Client(f"stream/{plug_num}")
  client.connect("localhost")
  print(f'plug/{plug_num}')
  client.subscribe(f'plug/{plug_num}')
  client.on_message=on_message

  # loop
  client.loop_start()  # Runs a loop in a background thread
  doc.add_periodic_callback(callback, 100)


plug_sessions = dict()

# https://docs.bokeh.org/en/latest/docs/user_guide/server.html
# section "Connecting with bokeh.client"
@app.route('/', methods=['GET'])
def bkapp_page():
  """ Uses existing server side page if one exists already, otherwise creates a
  new page and serves it to user. """
  args = request.args
  plug_num = int(args.get('plug')[0]) if 'plug' in args else 0

  if plug_num not in plug_sessions:
    session = pull_session(url='http://127.0.0.1:5006/bkapp', arguments=args)
    plug_sessions[plug_num] = session.id
    session.close()

  s = plug_sessions[plug_num]
  script = server_session(session_id=s, url='http://127.0.0.1:5006/bkapp')
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
