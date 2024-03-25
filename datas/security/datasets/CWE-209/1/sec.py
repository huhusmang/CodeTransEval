from flask import Flask
app = Flask(__name__)


import traceback

def do_computation():
    raise Exception("Secret info")

@app.route('/good')
def server_good():
    try:
        do_computation()
    except Exception as e:
        print(traceback.format_exc())
        return "An internal error has occurred!"