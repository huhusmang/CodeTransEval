from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/check_ip")
def check_ip():
    client_ip = request.headers.get("x-forwarded-for")
    if not client_ip.startswith("192.168."):
        raise Exception("ip illegal")
    return "ip legal"
