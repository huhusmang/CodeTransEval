from flask import Flask, redirect, request
import re

app = Flask(__name__)

@app.route('/redirect_to_target')
def redirect_to_target():
    target = request.args.get('target')
    if re.match(r'^https?://example\.com/', target):
        return redirect(target)
