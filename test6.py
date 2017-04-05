from flask import Flask, render_template
from flask import request
from random import randint
from time import time

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        values = {}
        values["result"] = int(request.form['value'])
        values["v1"] = int(request.form['v1'])
        values["v2"] = int(request.form['v2'])
        values["ellapsed"] = time() - float(request.form['timestamp'])
        if values["v1"] + values["v2"] == values["result"]:
            return render_template("result.html", value = values)
        else:
            values["timestamp"] = float(request.form['timestamp'])
            return render_template("form.html", vs = values)
    if request.method == 'GET':
        values = {}
        values["v1"] = randint(0, 100)
        values["v2"] = randint(0, 100)
        values["timestamp"] = time()
        values["ellapsed"] = 0
        return render_template("form.html", vs = values)


if __name__ == "__main__":
    app.run()
