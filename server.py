from flask import Flask, render_template, request, redirect, jsonify, session, flash
import os
from server.users import Users
from server.clients import Clients

app= Flask(__name__)

users = Users()
clients = Clients()
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if 'logged' in session:
        return redirect('/main')
    else:
        title = "Certify Me!"
        return render_template('index.html', title=title)
@app.route('/main')
def main():
    if 'logged' in session:
        return render_template('main.html')
    else:
        return redirect('/')
@app.route('/permission_partial')
def permission():
    print session
    if 'logged' in session:
        if session['permission'] == "super-admin":
            return redirect('/index/choose_client')
        else:
            return redirect('/index/add_class')
    else:
        #returns an error as AJAX response, which is handled in front end as a redirect the root route
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#partial loading routes
@app.route('/index/choose_client')
def client():
    title = "Choose a Client"
    all_clients = clients.findAll()
    return render_template('partials/client.html', title=title, all_clients=all_clients)
@app.route('/index/add_user')
def add_user():
    title = "Add a User"
    all_clients = clients.findAll()
    return render_template('partials/add_user.html', title=title, all_clients=all_clients)
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
@app.route('/login', methods=['POST'])
def login():
    logged = users.login(request.form)
    print "logged", logged
    if 'success' in logged:
        print "user ", logged['success'], " is logged in"
        print "user permission level is: ", logged['permission']
        return redirect('/main')
    else:
        print "error", logged['error']
        flash(logged['error'])
        return redirect('/')
@app.route('/add_user', methods=['POST'])
def add_user_form():
    return users.add(request.form)
@app.route('/add_client', methods=['POST'])
def add_client_form():
    return clients.add(request.form)
@app.route('/choose_client', methods=['POST'])
def choose_client():
    session['client_id'] = request.form['id']
    print "my current session data", session
    return redirect('/index/add_class')
app.run(debug=True)
