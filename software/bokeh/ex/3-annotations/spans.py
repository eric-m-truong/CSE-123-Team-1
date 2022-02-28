from bokeh.models import Span
from bokeh.plotting import figure, show

p = figure(x_axis_type="datetime", y_axis_type="datetime")
x = y = [i for i in range(10)]
p.line(x, y)
span1 = Span(location=2, # x-axis location
             dimension='height', line_color='#009E73',
             line_dash='dashed', line_width=3)
p.add_layout(span1)
span2 = Span(location=9,
             dimension='height', line_color='#F0E442',
             line_dash='dashed', line_width=3)
p.add_layout(span2)
show(p)
