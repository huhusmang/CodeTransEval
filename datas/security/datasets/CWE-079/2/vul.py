import flask
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

# function which says hello to the user
@app.route("hello")
def hello():
    username = request.args.get('username')
    return "Hello, " + username
