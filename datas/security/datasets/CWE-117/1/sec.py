from flask import Flask, request
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/logger')
def logger():
    '''
    get name data from the request and log it
    '''
    name = request.args.get('name')
    name = name.replace('\r\n','').replace('\n','')
    logging.info('name: %s', name)