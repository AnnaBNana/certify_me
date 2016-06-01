from flask import Flask, render_template, request, redirect, jsonify
from server.mysqlconnection import MySQLConnector

app= Flask(__name__)
postgresql = MySQLConnector(app, 'CertifyMe')

@app.route('/')
def index():
    title = "Certify Me!"
    return render_template('index.html', title=title)
#partial loading routes
@app.route('/index/login')
def login():
    title = "Choose a Client"
    return render_template('partials/client.html', title=title)
@app.route('/index/add_user')
def add_user():
    title = "Add a User"
    return render_template('partials/add_user.html', title=title)
@app.route('/index/add_client')
def add_client():
    title = "Add a Client"
    return render_template('partials/add_client.html', title=title)
#end partials
app.run(debug=True)
