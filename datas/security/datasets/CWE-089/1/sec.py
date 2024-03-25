from flask import Flask, request
import MySQLdb

app = Flask(__name__)

@app.route('/unsubscribe')
def unsubscribe():
    email = request.args.get('email')
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="db")
    cursor = db.cursor()
    
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))