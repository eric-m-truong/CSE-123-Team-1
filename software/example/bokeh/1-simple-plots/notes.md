# Simple plots

<https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_1.html>

```python
from bokeh.plotting import figure, show
```

- `figure(...)`: create a new, empty fig
  - `title`: str
  - `{x,y}_axis_label`: str
- `figure.line(x,y,...)`: render a line in a fig
  - `legend_label`: str
  - `color`: str
  - `line_width`: int
- `show(fig)`: render a fig in browser
