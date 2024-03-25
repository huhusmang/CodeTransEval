from flask import Flask, request, safe_join

app = Flask(__name__)

@app.route("/read")
def read():
    requested_file_name = request.args.get('filename')
    safe_dir = '/safe/'

    file_path = safe_join(safe_dir, requested_file_name)
    if file_path is None or not file_path.startswith(safe_dir):
        return "Invalid file path", 400

    file_content = open(file_path, 'r').read()

    return file_content
