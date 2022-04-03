from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/toggle/<plug>')
def control(plug):
  print(f'toggle {plug}')
  return '', 204

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
    print(plug)
    return '', 204 # return empty response
  else:
    return post

if __name__ == '__main__':
  app.run(debug = True)
