from flask import Flask, redirect, url_for, request
import paho.mqtt.client as mqtt


app = Flask(__name__)


def toggle_plug(plug):
  try:
    client = mqtt.Client("post")
    client.connect("localhost")
    plug = int(plug)
    client.publish("ctrl", plug)
  except ConnectionRefusedError:
    print("No broker running on localhost")


@app.route('/toggle/<plug>')
def toggle(plug):
  toggle_plug(plug)
  return '', 204 # return empty response


post = """
<form method="post">
  <input type="text" name="plug">
  <input type="submit" value="send signal">
</form>
"""


@app.route('/',methods = ['POST', 'GET'])
def submit():
  if request.method == 'POST':
    plug = request.form.get('plug')
    toggle_plug(plug)
    return '', 204 # return empty response
  else:
    return post


if __name__ == '__main__':
  app.run(debug = True)
