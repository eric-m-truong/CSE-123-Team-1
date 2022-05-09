from collections import defaultdict

import numpy as np
import pandas as pd

from bokeh.palettes import viridis
from bokeh.plotting import figure, save, show, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import DataRange1d

import sqlite3

from db.connection import connect, execute
from db.util import get_24h_avg_by_hr


def generate():
  """
  plots the past 24 hour hourly average for each plug. averaging is done in the
  db query itself.
  """

  con = connect()

  macs = [mac[0] for mac in execute(con, "SELECT mac_addr FROM Plugs")]
  HRS_DAY = 24
  data = {mac: np.zeros(HRS_DAY) for mac in macs}

  for hr, mac, avg in get_24h_avg_by_hr(con):
    data[mac][hr] = avg

  con.close()

  # Get list of keys now, before we add x data
  names = list(data.keys())

  data['ts'] = np.array(range(1, HRS_DAY + 1))

  p = figure(title='24h Electricity Usage History',
      sizing_mode='stretch_both',
      min_border=0,
      x_axis_label='hour(s) ago',
      y_axis_label='W',
      # bounds prevents 'pan' from scrolling out of the bounds of the data
      y_range=DataRange1d(bounds='auto'),
      x_range=DataRange1d(bounds=(1, HRS_DAY)),
      toolbar_location='below')
  p.grid.minor_grid_line_color = '#eeeeee'
  # Don't pad the ranges since these are thicc bloccs
  p.x_range.range_padding = p.y_range.range_padding = 0
  p.xaxis.ticker.desired_num_ticks = 24 # label all 24 ticks
  # Flip on the time axis so now is rightmost and the past is leftmost
  p.x_range.flipped = True

  p.varea_stack(names,
      color=viridis(len(names)),
      x='ts',
      legend_label=names,
      source=data)

  p.legend.orientation = "horizontal"
  p.legend.background_fill_color = "#fafafa"




  #p.axis.axis_label=None
  #p.axis.visible=False
  p.legend.orientation='vertical';
  p.grid.grid_line_color = None
  p.outline_line_color = None
  p.toolbar.logo = None
  p.toolbar_location = None
  p.sizing_mode='stretch_both';
  p.outline_line_alpha = 0;
  p.border_fill_alpha = 0;

  #print("HIS NAME IS ODDPARENT\n\n\n\n\n")
  #File Code
  output_file(filename="server/templates/stacked.html", title="Stacked HTML File")
  
  save(p)

  return file_html(p, CDN)
