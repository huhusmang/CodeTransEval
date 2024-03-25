import base64
from flask import Flask, request
app = Flask(__name__)

def setname(first_name):
    pass

@app.route("/code_execution")
def code_execution():
    first_name = base64.decodestring(request.args.get('first_name'))
    # call setname on first_name
    exec("setname('%s')" % first_name)
