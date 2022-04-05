`https://docs.bokeh.org/en/latest/docs/user_guide/server.html?highlight=periodic`

# running bokeh ex

`bokeh serve --show script.py`

## local broker

`mosquitto &` -v for verbose

## generating bogus data

`../../../script/datagen.py` publishes `ts,val` pairs to random plug #'s channel
`plug/#` at random intervals between 0-1

## stream

proof of concept that adapts an example from
`https://panel.holoviz.org/gallery/streaming/streaming_bokeh.html#streaming-gallery-streaming-bokeh`
to run locally and without panel

## stream_mqtt

consumes data from mqtt channel and uses it to update bokeh chart

# running

```
../../../script/stream_mqtt.sh 1 bokeh serve --show stream_mqtt.py
```

depends on:
- mosquitto
- python paho-mqtt
- bokeh

## stream_mqtt_nobuf

- does the chart update in the `on_message` callback
- it's _probably_ better to buffer data and update the graph less often, because
  updates require redrawing the graph entirely
