from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("hello.html", name="Anonymous")

@app.route('/user/<username>')
def show_user_profile(username):
    return render_template("hello.html", name=username)

if __name__ == "__main__":
    app.run()
