from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("form_test.html")

@app.route('/value', methods=["POST"])
def check_value():
    if request.method == 'POST':
        v = request.form['value']
        return render_template("hello.html", name=v)

if __name__ == "__main__":
    app.run()
