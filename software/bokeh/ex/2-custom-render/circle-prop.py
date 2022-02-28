from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y1 = [4, 5, 5, 7, 2]
y2 = [8, 2, 4, 1, 6]
p = figure(title="Circle properties example")
p.circle(x, y1,
  fill_color="red",     # circle body color
  fill_alpha=0.5,       # 0-1 transparency of circle body
  line_color="blue",    # color of circle outline
  size=80               # size of circles in screen units
)
p.circle(x, y2, fill_color="yellow", fill_alpha=0.3, line_color="green", size=9)
show(p)
