from bokeh.plotting import figure, show

x  = [1, 2, 3, 4, 5]
y1 = [6, 7, 2, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [4, 5, 5, 7, 2]
p = figure(title="Multiple bars example")
# top defines the single y-coord for each bar; stated more clearly, height
# bottom defines y-intercept, i.e. the 0 value where the lowest data pt starts
# width is fatness of each bar
p.vbar(x=x, top=y1, width=0.5, bottom=0, color="red")
p.vbar(x=x, top=y2, width=0.7, bottom=1, color="blue")
p.vbar(x=x, top=y3, width=0.9, bottom=2, color="green")
show(p)
