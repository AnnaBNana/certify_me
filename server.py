from flask import Flask, render_template, request, redirect, jsonify, session, flash
import os
from server.users import Users
from server.clients import Clients
from server.businesses import Businesses
from server.classes import Classes
from server.instructors import Instructors

app= Flask(__name__)

users = Users()
clients = Clients()
businesses = Businesses()
classes = Classes()
instructors = Instructors()
app.secret_key = os.urandom(24)
#base page loading routes: index, main, permissions check, logout
@app.route('/')
def index():
    if 'logged' in session:
        return redirect('/main')
    else:
        print session
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
        #returns an error as AJAX response, which is handled in front end as a redirect to the root route
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#begin partial loading routes
@app.route('/index/choose_client')
def client():
    if 'logged' in session:
        title = "Choose a Client"
        all_clients = clients.findAll()
        return render_template('partials/client.html', title=title, all_clients=all_clients)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/index/add_user')
def add_user():
    if 'logged' in session:
        title = "Add a User"
        all_clients = clients.findAll()
        return render_template('partials/add_user.html', title=title, all_clients=all_clients)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/index/add_biz')
def add_biz():
    if 'logged' in session:
        return render_template('partials/add_business.html')
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/index/add_client')
def add_client():
    if 'logged' in session:
        title = "Add a Client"
        all_businesses = businesses.findAll()
        return render_template('partials/add_client.html', title=title, businesses=all_businesses)
    else:
        error = {'error': 'redirect'}
        print error
        return jsonify(error)
@app.route('/index/add_class')
def add_class():
    if 'logged' in session:
        title = "Add a Seminar"
        instructor_list = instructors.findAll()
        return render_template('partials/add_class.html', title=title, instructors=instructor_list)
    else:
        error = {'error': 'redirect'}
        print "class adding error:", error
        return jsonify(error)
@app.route('/index/certificates')
def pdf():
    if 'logged' in session:
        title = "Generate Certificates"
        return render_template('partials/choose_pdf.html', title=title)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/index/test')
def test():
    title = "Test"
    result = classes.findAll()
    return render_template('partials/test.html', title=title, class_list=result)
#end partial loading routes
#begin post routes
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
    if 'logged' in session:
        return users.add(request.form)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/add_client', methods=['POST'])
def add_client_form():
    if 'logged' in session:
        return clients.add(request.form)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/choose_client', methods=['POST'])
def choose_client():
    if 'logged' in session:
        session['client_id'] = request.form['id']
        print "my current session data", session
        return redirect('/index/add_class')
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
@app.route('/add_class', methods=['POST'])
def new_class():
    if 'logged' in session:
        print "server file: ", request.form
        class_id = classes.add(request.form)
        session['class_id'] = class_id
        print "operation complete, id is: ", class_id
        if class_id == "error":
            return redirect('/index/add_class')
        else:
            return redirect('/index/certificates')
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
app.run(debug=True)
