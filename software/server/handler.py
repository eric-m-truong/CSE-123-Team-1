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


@app.route('/stream/<plug_num>', methods=['GET'])
def stream(plug_num):
  ip = config.broker['ip']
  user = config.broker['user']
  pw = config.broker['pass']

  con = connect()

  name_and_status = [(alias if alias else mac, status)
      for mac, alias, status in execute(con, "SELECT * FROM Plugs")]
  name, status = name_and_status[int(plug_num)]

  con.close()

  if not status:
    return f'{name} is disabled!'
  else:
    return render_template("mqtt_ws.html",
                           plug_name=name,
                           ip=ip, username=user, password=pw)


def toggle_plug(plug_num):
  try:
    client = mqtt.Client()
    client.username_pw_set(config.broker['user'], config.broker['pass'])
    client.connect(config.broker['ip'])
    print(plug_num)
    client.publish("ctrl", int(plug_num))
  except ConnectionRefusedError:
    print(f"No broker running on {config.broker['ip']}")


@app.route('/toggle/<plug_num>')
def toggle(plug_num):
  toggle_plug(plug_num)
  return '', 204 # return empty response


post = """
<form method="post">
  <input type="text" name="plug">
  <input type="submit" value="send signal">
</form>
"""


@app.route('/toggle', methods = ['POST', 'GET'])
def toggle_form():
  if request.method == 'POST':
    plug = request.form.get('plug')
    toggle_plug(plug)
    return '', 204 # return empty response
  else:
    return post


@app.route("/")
def root():
  links = []
  for r in app.url_map.iter_rules():
    links.append((str(r), r.endpoint))
  return render_template("sitemap.html", links=links)


@app.route("/lp")
def list_plugs():
  con = connect()
  plugs = [(alias if alias else mac, status)
      for mac, alias, status in execute(con, "SELECT * FROM Plugs").fetchall()]
  con.close()
  return render_template("lp.html", plugs=plugs)


@app.route("/alias", methods = ['POST', 'GET'])
def give_alias():
  # note: using indexes here would be brittle; imagine a plug was added in the
  # time the user took to select a plug and type its alias. instead, we opt to
  # pass the mac of the plug, alias or not
  if request.method == 'POST':
    plug = request.form.get('plug')
    alias = request.form.get('alias')
    con = connect()
    upd_alias(con, alias, plug)
    con.close()
    logging.debug(f'gave {plug} alias {alias}')
    return '', 204 # return empty response
  else:
    con = connect()
    plugs = [row[0] for row in # annoying: tuple of length 1
        execute(con, "SELECT mac_addr FROM Plugs").fetchall()]
    con.close()
    return render_template("alias.html", plugs=plugs)

if __name__ == '__main__':
  app.run(debug = True)
