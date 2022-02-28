from bokeh.plotting import figure, show

x  = [1, 2, 3, 4, 5]
y1 = [6, 7, 2, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [4, 5, 5, 7, 2]
p = figure(title="Scatter plot example")
p.circle(x, y1, color="blue")
p.circle(x, y2, color="red")
p.circle(x, y3, color="green")
show(p)
