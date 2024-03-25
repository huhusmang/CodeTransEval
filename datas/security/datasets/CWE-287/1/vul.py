from flask import Flask, session

app = Flask(__name__)
aConstant = 'CHANGEME1'
SECRET_KEY = aConstant
app.config.from_object(__name__)


@app.route('/')
def DEB_EX():
    if 'logged_in' not in session:
        session['logged_in'] = 'value'
    return app.secret_key, session.__str__()
