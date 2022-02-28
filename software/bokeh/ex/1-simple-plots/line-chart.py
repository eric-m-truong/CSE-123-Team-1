from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
p = figure(title="Single line example")
p.line(x, y)
show(p)
