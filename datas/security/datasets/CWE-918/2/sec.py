import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/partial_ssrf")
def partial_ssrf():
    user_id = request.args["user_id"]

    if user_id.isalnum():
        resp = requests.get("https://api.example.com/user_info/" + user_id)