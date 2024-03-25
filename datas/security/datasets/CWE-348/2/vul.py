from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/check_ip")
def check_ip():
    client_ip = request.headers.get("x-forwarded-for")
    if not client_ip == "127.0.0.1":
        raise Exception("ip illegal")
    return "ip legal"
