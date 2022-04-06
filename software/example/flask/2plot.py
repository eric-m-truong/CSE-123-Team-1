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


app = Flask(__name__)


def bkapp(doc):
  p = figure(sizing_mode='stretch_width', title='Bokeh streaming example')

  xs = np.arange(1000)
  ys = np.random.randn(1000).cumsum()
  x, y = xs[-1], ys[-1]

  cds = ColumnDataSource(data={'x': xs, 'y': ys})

  random255 = lambda: np.random.randint(255)
  color = tuple(random255() for _ in range(3))
  p.line('x', 'y', source=cds, color=color)

  def callback():
    nonlocal x, y
    # x, y are single values. when we add to them, we produce a new (x,y) pt
    x += 1
    y += np.random.randn()
    # append this new pt to the graph
    cds.stream({'x': [x], 'y': [y]})

  doc.add_root(column(p))
  doc.add_periodic_callback(callback, 100)


@app.route('/', methods=['GET'])
def bkapp_page():
    plot1 = server_document('http://127.0.0.1:5006/bkapp')
    plot2 = server_document('http://127.0.0.1:5006/bkapp')
    return render_template("2plot.html",
                           plot1=plot1,
                           plot2=plot2,
                           template="Flask")


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
