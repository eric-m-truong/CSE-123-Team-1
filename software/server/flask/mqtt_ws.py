from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def bkapp_page():
  args = request.args
  plug_num = int(args.get('plug')[0]) if 'plug' in args else 0
  return render_template("mqtt_ws.html", plug_num=plug_num)


if __name__ == '__main__':
    app.run(port=8000)
