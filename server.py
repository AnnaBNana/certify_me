from flask import Flask, render_template, request, redirect, jsonify, session, flash
from werkzeug import secure_filename
import os
import dropbox
#import models
from server.users import Users
from server.clients import Clients
from server.businesses import Businesses
from server.classes import Classes
from server.instructors import Instructors
from server.certificates import Certificates


app= Flask(__name__)


# assign model classes to variables
users = Users(app)
clients = Clients(app)
businesses = Businesses(app)
classes = Classes(app)
instructors = Instructors(app)
certificates = Certificates(app)
app.secret_key = os.urandom(24)


#dropbox settings
access_token = os.environ.get('ACCESS_TOKEN')
client = dropbox.client.DropboxClient(access_token)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'csv'])

certificates.parse('./static/uploads/Attendance_Results.csv')
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


@app.route('/check_pdf_url')
def check_pdf_url():
    if "logged" in session:
        client_id = session['client_id']
        url = businesses.check_pdf_url(client_id)
        if url == "":
            nourl = {'nourl': 'not found'}
            return jsonify(nourl)
        else:
            pdf_url = {'url': url}
            return jsonify(pdf_url)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#begin partial loading routes
@app.route('/index/add_user')
def add_user():
    if 'logged' in session:
        title = "Add a User"
        all_clients = clients.findAll()
        print all_clients
        return render_template('partials/add_user.html', title=title, all_clients=all_clients)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/users')
def view_users():
    if 'logged' in session:
        title = "All Users"
        all_users = users.findAll()
        return render_template('partials/users.html', title=title, users=all_users)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/user/<id>')
def show_user(id):
    print id
    if 'logged' in session:
        user = users.findOne(id)
        title = "Edit User Info"
        return render_template('partials/user.html', title=title, user=user)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/choose_client')
def choose_client():
    if 'logged' in session:
        title = "Choose a Client"
        all_clients = clients.findAll()
        return render_template('partials/choose_client.html', title=title, all_clients=all_clients)
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


@app.route('/index/clients')
def view_clients():
    if 'logged' in session:
        title = "All Clients"
        allClients = clients.findAll()
        return render_template('partials/clients.html', title=title, clients=allClients)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/client/<id>')
def show_client(id):
    if 'logged' in session:
        title = "Edit Client"
        client = clients.findOne(id)
        return render_template('partials/client.html', title=title, client=client)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/add_class')
def add_class():
    if 'logged' in session:
        title = "Add a Seminar"
        instructor_list = instructors.findAll()
        return render_template('partials/add_class.html', title=title, instructors=instructor_list)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/classes')
def view_classes():
    if 'logged' in session:
        title = "All Seminars"
        all_classes = classes.findAll()
        return render_template('partials/classes.html', title=title, classes=all_classes)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/class/<id>')
def show_class(id):
    if 'logged' in session:
        title = "Edit Seminar"
        one_class = classes.findOne(id)
        class_instructors = instructors.find_all_class_instructors(id)
        all_instructors = instructors.find_all_other(id)
        return render_template('partials/class.html', title=title, one_class=one_class, instructors=class_instructors, all_instructors=all_instructors)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/certificates')
def pdf():
    if 'logged' in session:
        title = "Generate Certificates"
        incomplete_classes = classes.findIncomplete()
        return render_template('partials/certificates.html', title=title, incomplete_classes=incomplete_classes)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/test')
def test():
    title = "Test"
    result = classes.findAll()
    return render_template('partials/test.html', title=title, class_list=result)


@app.route('/index/add_biz')
def add_biz():
    if 'logged' in session:
        return render_template('partials/add_business.html')
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
#end partial loading routes


#begin delete routes
@app.route('/delete/user/<id>')
def destroy_user(id):
    users.destroy(id)
    return redirect('/index/users')
#end delete routes


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
def activate_client():
    if 'logged' in session:
        session['client_id'] = request.form['id']
        print "my current session data", session
        if request.form['source'] == "add":
            return redirect('/index/add_class')
        elif request.form['source'] == "gen":
            return redirect('/index/certificates')
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


@app.route('/update_user', methods=['POST'])
def update_user():
    if 'logged' in session:
        success = users.update(request.form)
        return success
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/update_client', methods=['POST'])
def update_client():
    if 'logged' in session:
        # print request.form
        businesses.update(request.form)
        clients.update(request.form)
        success = {"success": "success"}
        return jsonify(success)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/update_class', methods=['POST'])
def update_class():
    print "form data: ", request.form
    if 'logged' in session:
        classes.update(request.form)
        success = {"success": "success"}
        return redirect('/index/classes')
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/certificates', methods=['POST'])
def generate_certificates():
    if 'logged' in session:
        print "form data: ", request.form
        client_id = session['client_id']
        print "files data: ", request.files
        # could be done with list comprehension?
        filearray = []
        upload_loc = "./static/uploads/"
        for file in request.files:
            new_file = request.files[file]
            filename = secure_filename(new_file.filename)
            new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filearray.append(new_file.filename)
        certificates.parse(os.path.join(app.config['UPLOAD_FOLDER'], filearray[0]))
        #since this takes so long, give client option to upload files to dropbox after the rest of the operations are complete

        # f0 = open(upload_loc + filearray[0], 'r')
        # client.put_file("/" + filearray[0], f0)
        # f1 = open(upload_loc + filearray[1], 'rb')
        # client.put_file("/" + filearray[1], f1)
        #after all operations complete, remove files from local file storage

        # something like this: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.filename))
        success = {'success': 'yay, you win!'}
        return jsonify(success)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


app.run(debug=True)
