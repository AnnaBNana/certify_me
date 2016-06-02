from flask import Flask, render_template, request, redirect, jsonify
from server.users import Users
from server.clients import Clients

app= Flask(__name__)

users = Users()
clients = Clients()

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
@app.route('/index/add_class')
def add_class():
    title = "Add a Seminar"
    return render_template('partials/add_class.html', title=title)
@app.route('/index/certificates')
def pdf():
    title = "Generate Certificates"
    return render_template('partials/choose_pdf.html', title=title)
#end partials
#form submission routes
@app.route('/add_user', methods=['POST'])
def add_user_form():
    return users.register(request.form)
@app.route('/add_client', methods=['POST'])
def add_client_form():
    return clients.register(request.form)
app.run(debug=True)
