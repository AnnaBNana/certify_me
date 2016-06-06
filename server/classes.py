from flask import Flask, session, flash
from server.psqlconnection import PSQLConnector
from server.instructors import Instructors

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')
instructors = Instructors()

class Classes(object):
    def add(self, form_data):
        print "form data", form_data
        validate = True
        if len(form_data['name']) < 6:
            flash("Name should be at lease 6 characters long", "name_error")
            validate = False
        if not form_data['duration'].isdigit():
            flash("Please enter a whole number", "duration_error")
            validate = False
        if len(form_data['date']) < 10:
            flash("Please enter correct date format", "date_error")
            validate = False
        if form_data['existing_instructor'] == "" and ('new_instructor' not in form_data or form_data['new_instructor'] == ""):
            print "instructor validation fail"
            flash("Please choose existing instructor or add at least one new instructor", "instructor_error")
            validate = False
        #make this requirement longer in deployment, length requirement shortened for testing
        if len(form_data['email_text']) < 4:
            print "email validation fail"
            flash("Email must be at least 4 characters in length", "email_error")
            validate = False
        if len(form_data['race_verbiage']) < 4:
            print "race validation fail"
            flash("Race verbiage must be at least 4 characters in length", "race_error")
            validate = False
        if not validate:
            print "validation fail"
            return "error"
        else:
            print "validation pass"
            instructor_list = []
            for k, v in form_data.iteritems():
                #check every key to see if it begins with new instructor
                if k.startswith('new_instructor'):
                    #if it does push value to a list
                    instructor_list.append(v)
            print instructor_list
            query = "INSERT INTO classes (name, duration, client_id, email_text, date, created_at, race_verbiage, cvpm_verbiage, status) VALUES (:name, :duration, :client_id, :email_text, :date, NOW(), :race_verbiage, :cvpm_verbiage, :status) RETURNING id"
            values = {
                "name": form_data['name'],
                "duration": form_data['duration'],
                "client_id": session['client_id'],
                "email_text": form_data['email_text'],
                "date": form_data['date'],
                "race_verbiage": form_data['race_verbiage'],
                "cvpm_verbiage": form_data['cvpm_verbiage'],
                "status": "incomplete"
            }
            # add class, return id
            class_id = postgresql.query_db(query, values)
            print class_id
            # add instructor names from list items to db as a group, return ids
            instructor_ids = instructors.add(instructor_list, class_id)
            print "instructor ids: ", instructor_ids
            # with returned ids, we then go and add entries to relational table
            query = "INSERT INTO class_instructor (instructor_id, class_id) VALUES (:instructor_id, :class_id) RETURNING instructor_id"
            for id in instructor_ids:
                values = {
                    "instructor_id": id,
                    "class_id": class_id
                }
                postgresql.query_db(instructor_query, instructor)
            print all_instructor_ids
            return class_id
    def findAll(self):
        query = "SELECT * FROM classes";
        classes = postgresql.query_db(query)
        return classes
    def findOne(self, class_id):
        query = "SELECT * FROM classes WHERE id=:class_id";
        values = {
            "class_id": class_id
        }
        one_class = postgresql.query_db(query, values)
        return one_class
