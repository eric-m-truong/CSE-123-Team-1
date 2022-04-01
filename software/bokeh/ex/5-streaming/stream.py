import numpy as np
from bokeh.plotting import curdoc, figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource


p = figure(sizing_mode='stretch_width', title='Bokeh streaming example')

xs = np.arange(1000)
ys = np.random.randn(1000).cumsum()
x, y = xs[-1], ys[-1]

cds = ColumnDataSource(data={'x': xs, 'y': ys})

p.line('x', 'y', source=cds)

def stream():
  # x, y are single values. when we add to them, we produce a new (x,y) pt
  global x, y
  x += 1
  y += np.random.randn()
  # append this new pt to the graph
  cds.stream({'x': [x], 'y': [y]})

curdoc().add_root(column(p))
curdoc().add_periodic_callback(stream, 100)
