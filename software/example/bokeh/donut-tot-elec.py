from collections import Counter
from math import pi

import pandas as pd

from bokeh.palettes import Paired
from bokeh.plotting import figure, show
from bokeh.transform import cumsum

# Data

x = Counter({
    'device 1': 70, 'device 2': 13, 'device 3': 120,
    'device 4': 30, 'device 5': 40, 'device 6': 40,
})

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
