from flask import Flask, render_template, request, redirect
from server.mysqlconnection import MySQLConnection

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/client')
def client():
    return render_template('client.html')
@app.route('/emails')
def emails():
    return render_template('emails.html')
@app.route('/uploads')
def uploads():
    return render_template('uploads.html')
@app.route('/list')
def list():
    return render_template('list.html')
@app.route('/view')
def view():
    return render_template('view.html')
@app.route('/edit')
def edit():
    return render_template('edit.html')
app.run(debug=True)
