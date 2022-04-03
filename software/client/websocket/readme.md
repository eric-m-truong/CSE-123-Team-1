# running

just have your browser open the pages while a data generator and broker are
running

```
../../script/stream_mqtt.sh 2 firefox page.html
```

# ws.html

listens to mqtt `plug/0` and prints data to javascript console

# mqtt

fully client side data updates. works like `ws.html`, but plots data using bokeh
