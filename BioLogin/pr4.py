#------------------------------------------------------------------------------------
#   BIOMETRIC LOGIN WITH KEYSTROKE DYNAMICS
#------------------------------------------------------------------------------------
import numpy as np
import random
import pymongo
from flask import Flask, render_template, request, make_response, redirect, url_for
from random import randint
from time import time
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from pymongo import MongoClient

MONGODB_URI = ""

client = MongoClient(MONGODB_URI)
db = client.get_default_database()
collection = db.add
app = Flask(__name__)

#Array with words that have different complexities (3, 4, 5, 6, 7 or more letters,
#and uppercase on the first or last letter)
words = ["mas", "uno", "pie", "ojo", "ajo", "oca", "sed", "dos",
        "tos", "luz", "voz", "tez", "uva", "pan", "mar", "oso", "ola",
        "sol", "pez", "col", "sal" , "paz", "cal", "rio", "res",
        "ron", "lio", "mes", "par", "tio", "mio", "pua", "mes",
        "sur", "bar", "ala", "res", "asa", "feo", "mike",
        "paso", "lana", "maja", "rana", "talla", "peso", "lama", "mala",
        "rama", "tapa", "piso", "lapa", "rata", "tasa", "poso",
        "lata", "mama", "raya", "taza", "puso", "lava", "mapa", "raza",
        "ambos", "ameba", "oliva", "spray", "azote", "rumbo", "orfeo",
        "tanto", "atado", "fisga", "llama", "ramal", "virar", "venir",
        "catre", "berna", "ronco", "ardor", "aduar", "limbo", "agape",
        "habito", "fabada", "danesa", "edicto", "fabula", "gacela",
        "habana", "macaco", "obesas", "quemar", "tabaco", "vacuna",
        "ubicuo", "tablas", "rabano", "jabato", "hachas", "baboso",
        "gabacho", "iberico", "jabalis", "obispal", "objetos",
        "sabados", "ucranio", "vocablo", "vibraba", "ubicado",
        "flamear", "flagelo", "dancing", "drogata", "drenaje",
        "murcielago", "rinocerontes", "extraterritorial",
        "hipopotamo", "natillas", "comadreja", "electrodomestico",
        "lavavajillas", "babuinos", "ornitorrinco", "orangutan",
        "afroamericanos", "macarrones", "pabellones"
        ]

#Classifier dumped from notebook
clf = joblib.load("classifier.pkl")

#Login for training
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        if (usuario == "martins" or usuario == "axel"):
            return redirect(url_for(".getWord", user = usuario, correct = 0))
        else:
            return render_template("loginTrain.html")
    if request.method == "GET":
        return render_template("loginTrain.html")

@app.route("/words", methods=["GET", "POST"])
def getWord():
    if request.method == "POST":
        db = {}
        db["user"] = request.form["user"]
        db["word"] = request.form["newWord"]
        db["average"] = request.form["average"]
        db["ellapsed"] = time() - float(request.form["timestamp"])
	#If word is correct, insert into database
        if db["word"] == request.form["word"]:
            collection.insert(db)
            return redirect(url_for(".getWord", user = db["user"], avg = db["average"], correct = 1, time = db["ellapsed"]))
        else:
            db["word"] = request.form["word"]
            db["username"] = request.form["user"]
            db["timestamp"] = float(request.form["timestamp"])
            return render_template("form.html", vs = db, correct = 0)
    if request.method == "GET":
        values = {}
        values["username"] = request.args.get("user")
        values["average"] = request.args.get("avg")
        values["word"] = random.choice(words) #Get random words from the array
        values["timestamp"] = time()
        values["ellapsed"] = 0
        return render_template("form.html", vs = values, correct = request.args.get("correct"), time = request.args.get("time"))

#Predicting user typing the word
@app.route("/pred", methods=["GET", "POST"])
def predictUser():
    if request.method == "POST":
        values = {}
        if(len(request.form["newWord"]) > 0):
            values["word"] = request.form["newWord"]
            values["average"] = request.form["average"]
            values["ellapsed"] = time() - float(request.form["timestamp"])
            if values["word"] == request.form["word"]:
                test = np.array([values["average"], values["ellapsed"], len(values["word"])])
                values["prediction"] = clf.predict(test)[0]
                return render_template("prediction.html", value = values)
            else:
                values["word"] = request.form["word"]
                values["timestamp"] = time()
                values["ellapsed"] = 0
                return render_template("formPredict.html", vs = values)
        else:
            values["word"] = request.form["word"]
            values["timestamp"] = time()
            values["ellapsed"] = 0
            return render_template("formPredict.html", vs = values)
    if request.method == "GET":
        values = {}
        values["word"] = random.choice(words) #Get random words from the array
        values["timestamp"] = time()
        values["ellapsed"] = 0
        return render_template("formPredict.html", vs = values)

#Exporting data to CSV
@app.route("/list", methods=["GET"])
def list():
    ops = collection.find()
    ss = ""
    for o in ops:
        try:
            ss += str(o["user"]) #Store user in database
            ss += ";"
            ss += str(o["word"]) #Store random word in database for defining complexity later
            ss += ";"
            ss += str(o["average"]) #Store keyup/keydown average time
            ss += ";"
            ss += str(o["ellapsed"]) #Store time it took to type the word
            ss += "\n"
        except Exception as e:
            pass
    output = make_response(ss)
    output.headers["Content-Disposition"] = "attachment; filename=words.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    app.run()
