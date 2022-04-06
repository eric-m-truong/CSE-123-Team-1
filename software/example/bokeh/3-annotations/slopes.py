from random import uniform
from bokeh.models import Slope
from bokeh.plotting import figure, output_file, show

gradient = 2
y_intercept = 10
xpts = [i for i in range(20)]
ypts = [gradient * xpts[i] + y_intercept + uniform(0, 4) for i in range(20)]

p = figure(width=450, height=450)
p.circle(xpts, ypts, size=5, color="skyblue") # circular dots
slope = Slope(gradient=gradient, # slope. not gradient. slope.
              y_intercept=y_intercept,
              line_color='orange',
              line_dash='dashed',
              line_width=3.5)
p.add_layout(slope)
show(p)
