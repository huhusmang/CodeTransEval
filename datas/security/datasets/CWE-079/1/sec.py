from flask import Flask, request, make_response, escape

app = Flask(__name__)

@app.route('/showName')
def name():
    first_name = request.args.get('name', '')
    return make_response("Your name is " + escape(first_name))