<https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_2.html>

# customizing renderers

[full list of renderable gyphs](https://docs.bokeh.org/en/latest/docs/reference/plotting/figure.html#bokeh.plotting.figure)

## circles

see `circle-prop.py`

```python
p.circle(x, y1,
  fill_color="red",     # circle body color
  fill_alpha=0.5,       # 0-1 transparency of circle body
  line_color="blue",    # color of circle outline
  size=80               # size of circles in screen units
)
```

## bars


- `top`: defines the single y-coord for each bar; stated more clearly, height
- `bottom`: defines y-intercept, i.e. the 0 value where the lowest data pt starts
- `width`: fatness of each bar
- [full list of bar props](https://docs.bokeh.org/en/latest/docs/reference/plotting/figure.html#bokeh.plotting.Figure.vbar)

```python
p.vbar(x=x, top=y1, width=0.5, bottom=0, color="red")
p.vbar(x=x, top=y2, width=0.7, bottom=1, color="blue")
```

also see `bar.py`

## colors

- `color` prop sets both `fill_color` and `line_color`
- can specify by:
  - "firebrick": [named colors](https://www.w3.org/TR/css-color-4/#named-colors)
  - "#00FF00": hex
  - (100, 100, 255): 3-tuple RGB
  - (100, 100, 255, 0.5) 4-tuple RGBA (Alpha)

## altering existing glyphs

assign a variable to a render statement (e.g. `circle = p.circle(...)` then
access a property with the render's `.glyph.[property]`

## further

- <https://docs.bokeh.org/en/latest/docs/user_guide/styling.html#userguide-styling-glyphs>
- <https://docs.bokeh.org/en/latest/docs/user_guide/styling.html#userguide-styling-visual-properties>
