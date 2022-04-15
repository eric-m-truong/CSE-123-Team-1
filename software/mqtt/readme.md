# listener

server thread that receives messages from plugs and updates the db

currently, only prints received messages

# datagen

`generate(plug_num)`:
- gen data for `n` # of plugs
- expects broker to be running on localhost default port
- send a plug # to channel "ctrl" to tog ON/OFF
- `mosquitto_pub -t ctrl -m 0` can manually send these ctrl messages

# todo

- [ ]  accumulate values in buffer
- [ ]  periodically flush to db
- [ ]  add MAC to `datagen`
