from collections import defaultdict

import numpy as np
import pandas as pd

from bokeh.palettes import viridis
from bokeh.plotting import figure, save, show
from bokeh.resources import CDN
from bokeh.embed import file_html

import sqlite3

from db.connection import connect, execute
from db.util import get_by_approx_ts, get_uniq_ts


def generate(query_range="-1 day"):
  """ Relies on the assumption that we have the same amount of data for each
  plug: for any given datetime, every plug should have data. This assumption
  WILL NOT HOLD in live data; e.g. adding a new plug while the server is
  running. """

  con = connect()

  tss = [ts[0] for ts in get_uniq_ts(con, query_range)]
  macs = [mac[0] for mac in execute(con, "SELECT mac_addr FROM Plugs")]

  # if a plug has a value at a given ts, it will be 0
  data = {mac: np.zeros(len(tss)) for mac in macs}

  for i, ts in enumerate(tss):
    for mac, pwr in get_by_approx_ts(con, ts):
      data[mac][i] = pwr

  con.close()

  for _, pwrs in data.items():
    pwrs[pwrs == 0] = np.average(pwrs)

  # Get list of keys now, before we add x data
  names = list(data.keys())

  # Convert date strings to datetime.date objects (nothing will plot otherwise)
  data['ts'] = np.array(tss, dtype='datetime64[s]')

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
