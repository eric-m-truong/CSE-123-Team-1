from flask import Flask, redirect, url_for, request, render_template, \
                  send_from_directory
import paho.mqtt.client as mqtt

from plot import donut_tot, stacked
from db.connection import connect, execute
import mqtt.config as config


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
  return render_template("mqtt_ws.html",
                         plug_num=int(plug_num),
                         ip=ip, username=user, password=pw)


def toggle_plug(plug_num):
  try:
    client = mqtt.Client("post") # may need to randomize name
    client.connect(config.broker['ip'])
    client.username_pw_set(config.broker['user'], config.broker['pass'])
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


@app.route('/toggle',methods = ['POST', 'GET'])
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
  return render_template("lp.html", plugs=plugs)


if __name__ == '__main__':
  app.run(debug = True)
