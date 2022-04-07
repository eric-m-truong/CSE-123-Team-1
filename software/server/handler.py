from flask import Flask, redirect, url_for, request, render_template, \
                  send_from_directory
import paho.mqtt.client as mqtt

from plot import donut_tot


app = Flask(__name__)


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/donut_tot')
def serve_donut_tot():
  return donut_tot.generate()


@app.route('/stream/<plug_num>', methods=['GET'])
def stream(plug_num):
  return render_template("mqtt_ws.html", plug_num=int(plug_num))


def toggle_plug(plug_num):
  try:
    client = mqtt.Client("post")
    client.connect("localhost")
    client.publish("ctrl", int(plug_num))
  except ConnectionRefusedError:
    print("No broker running on localhost")


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


if __name__ == '__main__':
  app.run(debug = True)