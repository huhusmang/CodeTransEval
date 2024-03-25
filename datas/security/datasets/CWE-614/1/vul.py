from flask import Flask, request, make_response, Response

app = Flask(__name__)


@app.route("/set_cookie")
def set_cookie():
    resp = make_response()
    resp.set_cookie("name", value="value")
    return resp
