from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y1 = [6, 7, 2, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [4, 5, 5, 7, 2]
p = figure(title="Multi line example w/ color")
p.line(x, y1, color="blue")
p.line(x, y2, color="red")
p.line(x, y3, color="green")
show(p)
