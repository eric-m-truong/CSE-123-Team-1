import random
from bokeh.models import BoxAnnotation
from bokeh.plotting import figure, show

x = y = [i for i in range(100)]
p = figure(title="Box annotation example")
line = p.line(x, y, line_color="#000000", line_width=2)
mid_box = BoxAnnotation(bottom=20, top=80, left=50, right=70,
                        fill_alpha=0.2, fill_color="#009E73")
p.add_layout(mid_box)
show(p)
