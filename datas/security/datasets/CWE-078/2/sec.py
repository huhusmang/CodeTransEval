from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

@app.route("/ls")
def ls():
    dirname = request.args.get('dirname')
    p = subprocess.Popen(["ls", dirname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out