from flask import Flask, session

app = Flask(__name__)
aConstant = 'CHANGEME1'
app.config['SECRET_KEY'] = aConstant
app.secret_key = aConstant
app.config.update(SECRET_KEY=aConstant)


@app.route('/')
def CheckForSecretKeyValue():
    return app.secret_key, session.get('logged_in')
