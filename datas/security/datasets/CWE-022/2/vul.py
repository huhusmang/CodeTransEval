from flask import Flask, request, send_file
import os

app = Flask(__name__)

# return the requested image from the folder "/images"
@app.route('/img')
def img():
    img_name = request.args.get('img_name')
    img_path = "images/" + img_name

    if os.path.isfile(img_path):
        return send_file(img_path)