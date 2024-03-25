from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def hello():
    target = request.args.get('target', '')
    target = target.replace('\\', '')
    if not urlparse(target).netloc:
        return redirect(target, code=302)
    return redirect('/', code=302)