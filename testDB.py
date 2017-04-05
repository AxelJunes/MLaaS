from flask import Flask, render_template
from flask import request, make_response
from random import randint
from time import time
from humbledb import Mongo, Document

class OP(Document):
    config_database = 'operation'
    config_collection = 'add'

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        op = OP()
        op["result"] = int(request.form['value'])
        op["v1"] = int(request.form['v1'])
        op["v2"] = int(request.form['v2'])
        op["ellapsed"] = time() - float(request.form['timestamp'])
        if int(op["v1"]) + int(op["v2"]) == int(op["result"]):
            with Mongo:
                OP.insert(op)
            return render_template("result.html", value = op)
        else:
            op["timestamp"] = float(request.form['timestamp'])
            return render_template("form.html", vs = op)
    if request.method == 'GET':
        values = {}
        values["v1"] = randint(0, 100)
        values["v2"] = randint(0, 100)
        values["timestamp"] = time()
        values["ellapsed"] = 0
        return render_template("form.html", vs = values)

@app.route('/list', methods=["GET"])
def list():
    with Mongo:
        ops = OP.find()
        print (ops)
        ss = ""
        for o in ops:
            try:
                ss += o["v1"]
                ss += ";"
                ss += o["v2"]
                ss += ";"
                ss += o["ellapsed"]
                ss += "\n"
            except Exception as e:
                pass
        output = make_response(ss)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

if __name__ == "__main__":
    app.run()
