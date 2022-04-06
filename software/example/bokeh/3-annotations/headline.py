from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
p = figure(title="Headline example")
p.title_location        = "left"
t                       = p.title
t.text                  = "Changing headline text example"
t.text_font_size        = "25px"
t.align                 = "right"
t.background_fill_color = "darkgrey"
t.text_color            = "white"
show(p)
