<https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_3.html>

# annotations

## attributes

- [legend](https://docs.bokeh.org/en/latest/docs/reference/models/annotations.html#bokeh.models.legend)
- [title](https://docs.bokeh.org/en/latest/docs/reference/models/annotations.html#bokeh.models.title)

- visual elements that make plot easier to read
- [more info](https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html#userguide-annotations)


## box

- bounds defined by left/right or top/bottom.
- only providing one bound (e.g. left but no right), box extends to edge of
  unspecified edge of plot

## labels

- label individual data pts
- couldn't find a way to pass lists individually to `labelset()`, use
  `columndatasource` to group labels
- see `labels.py`

## slope

draws line of best fit for data

```python
slope = slope(gradient=gradient, # slope. not gradient. slope.
              y_intercept=y_intercept,
              line_color='orange',
              line_dash='dashed',
              line_width=3.5)
```

## span

draws a vertical line

```python
span2 = span(location=9,
             dimension='height', line_color='#f0e442',
             line_dash='dashed', line_width=3)
p.add_layout(span2)
```

## potentially useful annotations i didn't write demo files for

- [colorbar](https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html#color-bars)
  : looks like a heatmap
- [polygon](https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html#polygon-annotations) (older sibling of box)
- [bands](https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html#bands)
  : highlight a complex range of many data points, like box or polygon but even
  more detail
- [whiskers](https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html#whiskers)
  : show where data pts fall and the margin of error
