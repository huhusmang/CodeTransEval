from flask import Flask, request

app = Flask(__name__)

@app.route("/read")
def read():
    requested_file_name = request.args.get('filename')
    safe_dir = '/safe/'

    file_path = safe_dir + requested_file_name
    file_content = open(file_path, 'r').read()

    return file_content