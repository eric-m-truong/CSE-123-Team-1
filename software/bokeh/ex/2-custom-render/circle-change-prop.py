from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y = [4, 5, 5, 7, 2]
p = figure(title="Glyphs properties example")
circle = p.circle(x,y)
circle.glyph.fill_color = "blue"
show(p)
