from bokeh.plotting import figure, show

x  = [1, 2, 3, 4, 5]
y1 = [4, 5, 5, 7, 2]
y2 = [2, 3, 4, 5, 6]
p = figure(title="Legend example")
line   =   p.line(x, y1, legend_label="line",   color="red")
circle = p.circle(x, y2, legend_label="circle", color="blue")
l = p.legend
l.location = "top_left"
l.title = "this is a title"
l.background_fill_color = "navy"
l.background_fill_alpha = 0.2
show(p)
