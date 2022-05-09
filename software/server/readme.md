# routing

route|desc
-----|----
/<path:path>|path is any file in `static` folder
/donut_tot|plug usage overall
/stacked|24h usage w/ plugs data stacked on top each other
/stream/<plug_num>|live plot of incoming websocket mqtt data, uses `templates/mqtt_ws.html`
/toggle/<plug_num>|sends <plug_num> to 'control' mqtt topic. does not redirect.
/toggle|loads a form to specify plug # to toggle
/|display sitemap
/lp|list plugs by mac or alias if applicable, status, and allows toggling. clicking a plug name redirects to /stream/<plug_num>. uses `templates/lp.html`

server routes are defined by the decorators above methods in `handler.py`:

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

# dirs

- `static` houses bokeh plots generated from db
- `templates` are filled in and sent to the client
