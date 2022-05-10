from math import pi
from pathlib import Path

import pandas as pd

from bokeh.palettes import viridis
from bokeh.plotting import figure, save
from bokeh.transform import cumsum
from bokeh.resources import CDN
from bokeh.embed import file_html

import sqlite3

from db.connection import connect, execute
from db.util import get_sum


def generate():
  con = connect()
  sum = get_sum(con)
  name_alias = {mac: alias if alias else mac
      # it occurs to me that this query will break if we change the order of the
      # rows in the table or s.t. similar
      for mac, alias, _ in execute(con, "SELECT * FROM Plugs").fetchall()}
  x = {name_alias[plug]: tot_pwr for plug, tot_pwr in sum}

  con.close()

  if len(x) == 0:
    return 'no plugs found in db'

  # Data

  data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'dev'})
  data['angle'] = data['value']/data['value'].sum() * 2*pi
  data['color'] = viridis(len(x))


  # Plotting code

  p = figure(title="Total Electricity Use",
      sizing_mode='stretch_both',
      tools="hover,save",
      tooltips="@dev: @value",
      toolbar_location='below')

  p.annular_wedge(x=0, y=1,
      inner_radius=0.2, outer_radius=0.4,
      start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
      line_color="white", fill_color='color',
      legend_field='dev', source=data)

  p.axis.axis_label = None
  p.axis.visible = False
  p.grid.grid_line_color = None
  p.toolbar.logo = None

  return file_html(p, CDN)
