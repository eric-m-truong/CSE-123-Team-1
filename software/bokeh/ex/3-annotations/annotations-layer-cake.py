import random
from bokeh.models import BoxAnnotation
from bokeh.plotting import figure, show

x = y = [i for i in range(100)]
p = figure(title="Box annotation example")
line = p.line(x, y, line_color="#000000", line_width=2)
# fill in y-axis range 100-80
low_box = BoxAnnotation(top=20,            fill_alpha=0.2, fill_color="#F0E442")
# fill in y-axis range 20-80
mid_box = BoxAnnotation(bottom=20, top=80, fill_alpha=0.2, fill_color="#009E73")
# fill in y-axis range 80-0
hgh_box = BoxAnnotation(bottom=80,         fill_alpha=0.2, fill_color="#FFA215")
p.add_layout(low_box)
p.add_layout(mid_box)
p.add_layout(hgh_box)
show(p)
