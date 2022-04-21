from collections import defaultdict

import numpy as np
import pandas as pd

from bokeh.palettes import viridis
from bokeh.plotting import figure, save, show
from bokeh.resources import CDN
from bokeh.embed import file_html

import sqlite3

from db.connection import connect, execute
from db.util import get_24h, get_uniq_ts


def generate():
  """ Relies on the assumption that we have the same amount of data for each
  plug: for any given datetime, every plug should have data. This assumption
  WILL NOT HOLD in live data; e.g. adding a new plug while the server is
  running. """

  con = connect()
  cur = get_24h(con)

  QUERY_RANGE = "WHERE timestamp >= date('now', '-1 day')"

  tss = [ts[0] for ts in get_uniq_ts(con, QUERY_RANGE)]
  data = defaultdict(list)

  for pid, pwr in cur:
    data[pid].append(pwr)

  con.close()

  # Get list of keys now, before we add x data
  names = list(data.keys())

  # Convert date strings to datetime.date objects (nothing will plot otherwise)
  data['ts'] = np.array(list(tss), dtype=np.datetime64)

  p = figure(title='24h Electricity Usage History',
      sizing_mode='scale_both',
      min_border=0,
      x_axis_label='hr',
      x_axis_type='datetime',
      y_axis_label='W')
  p.grid.minor_grid_line_color = '#eeeeee'
  # Don't pad the ranges since these are thicc bloccs
  p.x_range.range_padding = p.y_range.range_padding = 0
  # Flip on the time axis so now is rightmost and the past is leftmost
  p.x_range.flipped = True

  p.varea_stack(names,
      color=viridis(len(names)),
      x='ts',
      legend_label=names,
      source=data)

  p.legend.orientation = "horizontal"
  p.legend.background_fill_color = "#fafafa"

  return file_html(p, CDN)
