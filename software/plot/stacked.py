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


def generate():
  """ Relies on the assumption that we have the same amount of data for each
  plug: for any given datetime, every plug should have data. This assumption
  WILL NOT HOLD in live data; e.g. adding a new plug while the server is
  running. """

  query_range = "-1 day"

  con = connect()

  tss = [ts[0] for ts in get_uniq_ts(con, query_range)]
  macs = [mac[0] for mac in execute(con, "SELECT mac_addr FROM Plugs")]

  data = defaultdict(list)

  for ts in tss:
    # if a plug has a value at that ts, use it, else set it to 0
    # just so happens that "default" int() is 0
    pwr_at_approx_ts = defaultdict(int)
    for mac, pwr in get_by_approx_ts(con, ts):
      pwr_at_approx_ts[mac] = pwr
    for mac in macs:
      data[mac].append(pwr_at_approx_ts[mac])

  con.close()

  # Get list of keys now, before we add x data
  names = list(data.keys())

  assert all(map(lambda x: len(x) == len(tss), data.values())), \
         "# uniq ts != # pts for all plugs"

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
