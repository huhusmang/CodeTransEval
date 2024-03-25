from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/ls")
def ls():
    dirname = request.args.get('dirname')
    command = "ls " + dirname
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    return out
