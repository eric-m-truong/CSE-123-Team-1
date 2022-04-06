`static` houses bokeh plots generated from db
`templates` are filled in and sent to the client

server paths are defined by the decorators above methods in `handler.py`:

```
@app.route('/stream/<plug_num>', methods=['GET'])
@app.route('/toggle/<plug_num>')
@app.route('/toggle',methods = ['POST', 'GET'])
```

so in the above we see that `/stream/0` would serve us a page that calls 
`stream(plug_num)` with the argument 0

we can access the html files in `static/` by their name. `/nothing.html` will
serve the file of that name.

we can request fresh copies of charts from the `plot` module on page load, e.g.
`/donut_tot`
