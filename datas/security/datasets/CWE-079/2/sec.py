import flask
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/hello")
def hello():
    username = request.args.get('username')
    username = flask.escape(username)
    return "Hello, " + username
