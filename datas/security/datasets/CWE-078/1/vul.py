from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

# ping a URL to see if it is alive using "ping" system command
@app.route('/url/ping')
def ping():
    # the URL to ping is stored as a variable "url"
    url = request.args.get('url')
    # run the ping command using the system command "ping"
    command = "ping -c 1 " + url
    # run the command and store the output
    output = subprocess.check_output(command, shell=True)
    # return the output to the user
    return output