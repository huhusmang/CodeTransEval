import base64
from flask import Flask, request
app = Flask(__name__)

def setname(first_name):
    pass

@app.route("/code_execution")
def code_execution():
    first_name = base64.b64decode(request.args.get('first_name')).decode('utf-8')
    setname(first_name)
