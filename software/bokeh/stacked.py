import numpy as np
import pandas as pd

from bokeh.palettes import brewer
from bokeh.plotting import figure, show

N = 8
df = pd.DataFrame(np.random.randint(10, 100, size=(24, N))).add_prefix('dev')

p = figure(title='24h Electricity Usage History',
    x_range=(0, len(df)-1),
    y_range=(0, 800),
    x_axis_label='hr',
    y_axis_label='W')
p.grid.minor_grid_line_color = '#eeeeee'

names = [f'dev{i}' for i in range(N)]
p.varea_stack(stackers=names,
    x='index',
    color=brewer['Spectral'][N],
    legend_label=names,
    source=df)

p.legend.orientation = "horizontal"
p.legend.background_fill_color = "#fafafa"

show(p)
