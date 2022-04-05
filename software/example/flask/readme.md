these flask pages demonstrate easily embeddable plots. check `templates` for the
`.html` these graphs are embedded in. it should be easy to expand them.

run these with

```
../../script/stream_mqtt.sh python script.py
```

# 2chart

demos 2 live charts at once

# mqtt

a single graph using mqtt to stream data

opening multiple pages fails because the server creates a new server-side page
for each session, and mqtt requires unique client ids. this is inefficient, too,
since the server must potetially listen to the same channel for multiple clients
at the same time

# mqtt_multi

view a specific plug by appending parameters to the server url

expected to be run with 1+ plugs sending data, e.g.

```
../../script/stream_mqtt.sh 2 python mqtt_multi.py &
```

then open the following pages

```
http://127.0.0.1:8000/?plug=0
http://127.0.0.1:8000/?plug=1
http://127.0.0.1:8000/?plug=2
```

0 and 1 should generate separate data, and 2 doesn't exist, so there should be
no data

note also that you may duplicate any of these tabs because this script caches
server-side pages by plug #, unlike `mqtt.py`

# Sidenote: part of streaming is server side, but is wasteful

bokeh forces us to listen to mqtt connections server side when it could be done
in the client side. i can't find a python solution that would generate
javascript callbacks from python, however.

Ajax seems like a way to keep stuff client side but seems more involved

E.g. <https://docs.bokeh.org/en/latest/docs/user_guide/data.html?highlight=ajax#ajaxdatasource>

# mqtt_ws

- uses websockets
- fully client side
- run like `mqtt_multi`, specify which plug in same way

# post

equivalent to `../django/post`, plus `localhost/toggle/[plug_num]` causes
callback to connect to mqtt server and send plug # to topic `ctrl`
