from flask import Flask, request, redirect
import MySQLdb
from flask import session

app = Flask(__name__)

@app.route('/buy_order', methods=['POST'])
def buy_stock():
    stock_name = request.form['stock_name']
    stock_quantity = request.form['stock_quantity']
    username = session['username']

    #insert the buy order in the database
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO buy_order (stock_name, stock_quantity, username) VALUES ('" + stock_name + "', '" + stock_quantity + "', '" + username + "')")
    db.commit()
    db.close()