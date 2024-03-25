from flask import Flask, request, make_response, Response


app = Flask(__name__)


@app.route("/set_cookie")
def set_cookie():
    resp = make_response("hello")
    resp.headers["Set-Cookie"] = "name=value;"
    return resp
