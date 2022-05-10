from flask import Flask, redirect, url_for, request, render_template, \
                  send_from_directory
import paho.mqtt.client as mqtt

from plot import donut_tot, stacked
from db.connection import connect, execute
from db.util import upd_alias
from mqtt import config
import logging


app = Flask(__name__)


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/donut_tot')
def serve_donut_tot():
  return donut_tot.generate()


@app.route('/stacked')
def serve_stacked():
  return stacked.generate()


@app.route('/stream/<plug_num>', methods=['POST','GET'])
def stream(plug_num):
  ip = config.broker['ip']
  user = config.broker['user']
  pw = config.broker['pass']
  port = config.broker['port']['websocket']
  useSSL = config.broker['useSSL']

  con = connect()

  plugs = [(mac, alias if alias else mac, status)
      for mac, alias, status in execute(con, "SELECT * FROM Plugs")]

  con.close()

  try:
    mac, name, status = plugs[int(plug_num)]
  except (IndexError, ValueError):
    return 'no such plug'

  if not status:
    return f'{name} is disabled!'
  else:
    return render_template("powersolo.html",
                          plug_name=name,
                          mac=mac,
                          ip=ip,
                          port=port,
                          useSSL=useSSL,
                          username=user,
                          password=pw)


@app.route('/toggle', methods = ['POST'])
def toggle():
  mac = request.form.get('mac')
  status = request.form.get('status')

  try:
    client = mqtt.Client()
    client.username_pw_set(config.broker['user'], config.broker['pass'])
    client.connect(config.broker['ip'])
    topic = f'plux/control/{mac}'
    logging.debug(f'sending {status} to {topic}')
    client.publish(topic, int(status))
  except ConnectionRefusedError:
    print(f"No broker running on {config.broker['ip']}")

  return '', 204 # return empty response


@app.route("/map")
def site_map():
  links = []
  for r in app.url_map.iter_rules():
    links.append((str(r), r.endpoint))
  return render_template("sitemap.html", links=links)


@app.route("/list")
def root():
  ip = config.broker['ip']
  user = config.broker['user']
  pw = config.broker['pass']
  port = config.broker['port']['websocket']
  useSSL = config.broker['useSSL']

  con = connect()
  plugs = [(mac, alias if alias else mac, status)
      for mac, alias, status in execute(con, "SELECT * FROM Plugs").fetchall()]
  con.close()

  if len(plugs) == 0:
    return 'no plugs found in db'

  return render_template("powerlist.html",
                         plugs=plugs,
                         ip=ip,
                         port=port,
                         useSSL=useSSL,
                         username=user,
                         password=pw)


@app.route("/")
def home():
  ip = config.broker['ip']
  user = config.broker['user']
  pw = config.broker['pass']
  port = config.broker['port']['websocket']
  useSSL = config.broker['useSSL']

  con = connect()
  plugs = [(mac, alias if alias else mac, status)
      for mac, alias, status in execute(con, "SELECT * FROM Plugs").fetchall()]
  con.close()

  return render_template("power.html",
                         plugs=plugs,
                         donut=donut_tot.generate(),
                         stacked=stacked.generate(),
                         ip=ip,
                         port=port,
                         useSSL=useSSL,
                         username=user,
                         password=pw)


@app.route("/alias", methods = ['POST', 'GET'])
def give_alias():
  # note: using indexes here would be brittle; imagine a plug was added in the
  # time the user took to select a plug and type its alias. instead, we opt to
  # pass the mac of the plug, alias or not
  if request.method == 'POST':
    mac = request.form.get('mac')
    alias = request.form.get('alias')
    con = connect()
    upd_alias(con, alias, mac)
    con.close()
    logging.debug(f'gave {mac} alias {alias}')
    return '', 204 # return empty response
  else:
    con = connect()
    plugs = [row[0] for row in # annoying: tuple of length 1
        execute(con, "SELECT mac_addr FROM Plugs").fetchall()]
    con.close()

    if len(plugs) == 0:
      return 'no plugs found in db'

    return render_template("alias.html", plugs=plugs)


if __name__ == '__main__':
  app.run(debug = True)
