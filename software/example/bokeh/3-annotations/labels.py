from bokeh.models import ColumnDataSource, LabelSet, Range1d
from bokeh.plotting import figure, show

data = {'x': [0, 1, 2], 'y': [0, 1, 2], 'labels': ['Hello', 'World', 'Good']}
source = ColumnDataSource(data)
# x_range so we can see last label
p = figure(title='Labels example', x_range=Range1d(0, 2.5))
# x and y are labels as specified in data dict of ColumnDataSource
p.scatter(x='x', y='y', source=source)
labels = LabelSet(x='x', y='y', text='labels', source=source)
p.add_layout(labels)
show(p)
