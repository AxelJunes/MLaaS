from flask import Flask, render_template
from flask import request
from random import randint

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        v = request.form['value']
        p
    if request.method == 'GET':
        values = {}
        values["v1"] = randint(0, 100)
        values["v2"] = randint(0, 100)
        return render_template("form.html", vs = values)


if __name__ == "__main__":
    app.run()
