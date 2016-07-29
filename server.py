from flask import Flask, render_template, request, redirect, jsonify, session, flash
import os

#import models
from conf.attendees import Attendees
from conf.businesses import Businesses
from conf.certificates import Certificates
from conf.classes import Classes
from conf.clients import Clients
from conf.dropboxconnection import Dropbox
from conf.instructors import Instructors
from conf.sendgridconnection import SendgridConnection
from conf.users import Users


app= Flask(__name__)
app.secret_key = os.urandom(24)
db = "CertifyMe"

# assign model classes to variables
attendees = Attendees(app, db)
businesses = Businesses(app, db)
certificates = Certificates(app, db)
classes = Classes(app, db)
clients = Clients(app, db)
dropbox = Dropbox(app)
instructors = Instructors(app, db)
sendgrid = SendgridConnection(app)
users = Users(app, db)


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
        user_id = session['user_id']
        print "this is my user id: ", user_id
        user = users.findOne(user_id)
        print "this is my user info: ", user
        return render_template('main.html', user=user)
    else:
        return redirect('/')


@app.route('/permission_partial')
def permission():
    print "this is my full session data", session
    if 'logged' in session:
        if session['permission'] == "super-admin":
            return redirect('/index/choose_business')
        else:
            return redirect('/index/add_class')
    else:
        #returns an error as AJAX response, which is handled in front end as a redirect to the root route
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/check_pdf_url')
def check_pdf_url():
    if "logged" in session:
        business_id = session['business_id']
        url = businesses.check_pdf_url(business_id)
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
        biz = businesses.findAll()
        print biz
        return render_template('partials/add_user.html', title=title, all_clients=biz)
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


@app.route('/index/choose_business')
def choose_business():
    if 'logged' in session:
        title = "Choose a Business"
        all_businesses = businesses.findAll()
        return render_template('partials/choose_client.html', title=title, all_businesses=all_businesses)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/add_client')
def add_client():
    if 'logged' in session:
        title = "Add a Business"
        all_businesses = businesses.findAll()
        return render_template('partials/add_client.html', title=title, businesses=all_businesses)
    else:
        error = {'error': 'redirect'}
        print error
        return jsonify(error)


@app.route('/index/clients')
def view_clients():
    if 'logged' in session:
        title = "All Businesses"
        all_businesses = businesses.findAll()
        return render_template('partials/clients.html', title=title, businesses=all_businesses)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/client/<id>')
def show_client(id):
    if 'logged' in session:
        title = "Edit Business"
        owners = clients.find_biz_owners(id)
        business = businesses.findOne(id)
        return render_template('partials/client.html', title=title, business=business, clients=owners)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/add_class')
def add_class():
    if 'logged' in session:
        title = "Add a Seminar"
        business_id = session['business_id']
        instructor_list = instructors.findAll(business_id)
        return render_template('partials/add_class.html', title=title, instructors=instructor_list)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/classes')
def view_classes():
    if 'logged' in session:
        title = "All Seminars"
        id = session['business_id']
        all_classes = classes.findAll(id)
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
        print all_instructors
        return render_template('partials/class.html', title=title, one_class=one_class, instructors=class_instructors, all_instructors=all_instructors)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/certificates')
def pdf():
    if 'logged' in session:
        title = "Generate Certificates"
        business_id = session['business_id']
        incomplete_classes = classes.find_all_for_biz(business_id)
        return render_template('partials/certificates.html', title=title, incomplete_classes=incomplete_classes)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/index/mail')
def mail():
    if 'logged' in session:
        title = "Send Emails"
        class_id = session['class_id']
        students = attendees.find_all_in_class(class_id)
        return render_template('partials/mail.html', title=title, students=students)
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


@app.route('/index/dropbox_upload')
def dropbox_upload():
    if 'logged' in session:
        class_id = session['class_id']
        business_id = session['business_id']
        biz_data = businesses.findOne(business_id)
        class_data = classes.findOne(class_id)
        if dropbox.save_all(biz_data, class_data):
            message = {'success': 'All files uploaded'}
        else:
            message = {'upload_error': "files not uploaded"}
        return jsonify(message)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)
#end partial loading routes


#begin delete routes
@app.route('/delete/user/<id>')
def destroy_user(id):
    users.destroy(id)
    return redirect('/index/users')

@app.route('/delete/client/<id>')
def destroy_owner(id):
    clients.destroy(id)
    return redirect('/index/clients')
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
        message = users.add(request.form)
        return jsonify(message)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/add_client', methods=['POST'])
def add_client_form():
    if 'logged' in session:
        message = {}
        #handle case of existing biz
        if 'existing_biz' in request.form:
            biz_id = request.form['existing_biz']
        else:
            biz_data = businesses.add(request.form)
            if 'message' in biz_data:
                message = biz['message']
            elif 'biz_id' in biz_data:
                biz_id = biz_data['biz_id']
        if biz_id:
            client_msg = clients.add(biz_id, request.form)
            message = client_msg
        return jsonify(message)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/choose_business', methods=['POST'])
def activate_client():
    if 'logged' in session:
        session['business_id'] = request.form['id']
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
        messages = classes.add(request.form)
        if "id" not in messages:
            return jsonify(messages)
        else:
            session['class_id'] = messages['id']
            return redirect('/index/certificates')
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/update_user', methods=['POST'])
def update_user():
    if 'logged' in session:
        message = users.update(request.form)
        return jsonify(message)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/update_password', methods=['POST'])
def update_password():
    if 'logged' in session:
        id = session['user_id']
        message = users.update_password(request.form, id)
        return jsonify(message)
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
        business_id = session['business_id']
        class_id = request.form['class']
        session['class_id'] = class_id
        business = businesses.findOne(business_id)
        # save files to temp local storage, return file names array
        files = certificates.save_files(request.files)
        print request.form
        if request.form['existing_pdf']:
            pdf = request.form['existing_pdf']
            # will return error if doc not found in client's dropbox folder
            message = dropbox.get_file(pdf, business);
            # if file can't be found, terminate the rest of the process, prompt user to uplaod new file
            if 'file_error' in message:
                return jsonify(message)
        for file_name in files:
            if file_name.endswith('.csv'):
                csv_data = {
                    "csv_file": file_name,
                    "class_id": class_id
                }
                certificates.parseCSV(csv_data)
            elif file_name.endswith('.pdf'):
                pdf = file_name
                business_data = {
                    "pdf": pdf,
                    "id": business_id
                }
                businesses.add_pdf_url(business_data)
        students = attendees.get_cert_data(class_id)
        inst = instructors.find_all_class_instructors(class_id)
        pdf_data = {
            "class_id": class_id,
            "business_id": business_id,
            "template_pdf": pdf,
            "students": students,
            "inst": inst
        }
        messages_array = certificates.generate(pdf_data)
        messages = {'messages': messages_array}
        return jsonify(messages)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/update_email', methods=['POST'])
def update_email():
    if 'logged' in session:
        class_id = session['class_id']
        email_text = request.form['email_text']
        classes.update_email(email_text, class_id)
        success = {'success': 'yay, you win!'}
        return jsonify(success)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


@app.route('/send_mail', methods=['POST'])
def send_mail():
    if 'logged' in session:
        # request.form is a dict containing all student id's
        # key and value are the id
        print request.form
        class_id = session['class_id']
        business_id = session['business_id']
        business_data = businesses.findOne(business_id)
        class_data = classes.findOne(class_id)
        for id in request.form:
            student_data = attendees.findOne(id)
            if sendgrid.send(business_data, class_data, student_data):
                message = {'success': 'mail sent'}
            else:
                message = {'send_error': 'mail not sent'}
        return jsonify(message)
    else:
        error = {'error': 'redirect'}
        return jsonify(error)


app.run(debug=True)
