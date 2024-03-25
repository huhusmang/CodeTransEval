from flask import request, Flask
import re

app = Flask(__name__)


@app.route("/direct")
def direct():
    pattern = request.args['pattern']
    pattern = re.escape(pattern)
    re.search(pattern, "")


@app.route("/compile")
def compile():
    pattern = request.args['pattern']
    pattern = re.escape(pattern)
    compiled_pattern = re.compile(pattern)
    compiled_pattern.search("")