from flask import Flask, render_template
from flask import request, make_response
from random import randint
from time import time
from humbledb import Mongo, Document
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
import numpy as np

class OP(Document):
    config_database = 'operation'
    config_collection = 'add'

app = Flask(__name__)

#Classifier dumped from notebook
clf = joblib.load("classifier.pkl")

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        op = OP()
        op["result"] = int(request.form['value'])
        op["v1"] = int(request.form['v1'])
        op["v2"] = int(request.form['v2'])
        op["ellapsed"] = time() - float(request.form['timestamp'])
        #Calculate complexity of operation
        #-----------------------------------------------------------------------
        if(op["v1"]<10 and op["v2"]<10): #Both have 1 digit
            complexity = 0
        elif(op["v1"]==0 or op["v2"]==0): #One of the values is 0
            complexity = 1
        elif(op["v1"]%10==0 and op["v2"]%10==0): #Both can be divided by 10
            complexity = 2
        elif(op["v1"]<10 or op["v2"]<10): #Both have 1 digit
            complexity = 3
        elif((op["v1"] + op["v2"])%10==0): #Sum divided by 10 is 0
            complexity = 4
        elif(op["v1"]%2==0 and op["v2"]%2==0): #Both are even
            complexity = 5
        elif(op["v1"]%2==0 and op["v2"]%2==1): #One of them is even
            complexity = 6
        elif(op["v1"]%2==1 and op["v2"]%2==0): #One of them is even
            complexity = 6
        elif(op["v1"]%2==1 and op["v2"]%2==1): #Both are odd
            complexity = 7
        #-----------------------------------------------------------------------
        prediction = clf.predict(complexity)[0]
        if int(op["v1"]) + int(op["v2"]) == int(op["result"]):
            with Mongo:
                OP.insert(op)
            return render_template("result.html", value = op, pred = prediction)
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
        ss = ""
        for o in ops:
            try:
                ss += str(o["v1"])
                ss += ";"
                ss += str(o["v2"])
                ss += ";"
                ss += str(o["ellapsed"])
                ss += "\n"
            except Exception as e:
                pass
        output = make_response(ss)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

if __name__ == "__main__":
    app.run()
