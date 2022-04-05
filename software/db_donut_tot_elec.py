from math import pi
from pathlib import Path

import pandas as pd

from bokeh.palettes import Paired
from bokeh.plotting import figure, show
from bokeh.transform import cumsum

import sqlite3

DATA_DIR = '../data/'
DB_NAME = 'data.sqlite'
DB_PATH = DATA_DIR + DB_NAME

if not Path(DB_PATH).exists():
  import db_datagen # haha don't actually use in production

connection = sqlite3.connect()
cursor = connection.cursor()
cursor.execute("SELECT plug_id, SUM(power) FROM Data GROUP BY plug_id")

x = {plug: tot_pwr for plug, tot_pwr in cursor.fetchall()}

connection.close()

# Data

data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'dev'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Paired[len(x)]


# Plotting code

p = figure(plot_height=350, title="Total Electricity Use",
    toolbar_location=None,
    tools="hover",
    tooltips="@dev: @value",
    x_range=(-0.5, 1.0))

p.annular_wedge(x=0, y=1,
    inner_radius=0.2, outer_radius=0.4,
    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    line_color="white", fill_color='color',
    legend_field='dev', source=data)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None

show(p)
