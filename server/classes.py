from flask import session
import re
from server.psqlconnection import PSQLConnector
from server.instructors import Instructors


class Classes(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')
        self.instructors = Instructors(app)


    def add(self, form_data):
        print "form data", form_data
        validate = True
        course_regex = re.compile(r'^(\d+)-(\d+)')
        match_obj = re.match(course_regex, form_data['course_num'])
        instructor_list = []
        for k, v in form_data.iteritems():
            #check every key to see if it begins with new instructor
            if k.startswith('new_instructor'):
                #if it does push value to a list
                instructor_list.append(v)
        if len(form_data['name']) < 6:
            flash("Name should be at lease 6 characters long", "name_error")
            validate = False
        if not match_obj:
            flash("Expected digits-digits format, please check course number", "course_num_error")
        if not form_data['duration'].isdigit():
            flash("Please enter a whole number", "duration_error")
            validate = False
        if len(form_data['date']) < 10:
            flash("Please enter correct date format", "date_error")
            validate = False
        if form_data['existing_instructor'] == "" and len(instructor_list) < 1:
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
            print instructor_list
            query = "INSERT INTO classes (name, duration, client_id, email_text, date, created_at, race_verbiage, cvpm_verbiage, status, race_course_num) VALUES (:name, :duration, :client_id, :email_text, :date, NOW(), :race_verbiage, :cvpm_verbiage, :status, :race_course_num) RETURNING id"
            values = {
                "name": form_data['name'],
                "duration": form_data['duration'],
                "client_id": session['client_id'],
                "email_text": form_data['email_text'],
                "date": form_data['date'],
                "race_verbiage": form_data['race_verbiage'],
                "cvpm_verbiage": form_data['cvpm_verbiage'],
                "status": "incomplete",
                "race_course_num": form_data['course_num']
            }
            # add class, return id
            class_id = self.postgresql.query_db(query, values)
            print class_id
            # add instructor names from list items to db as a group, return ids
            instructor_ids = self.instructors.add(instructor_list, class_id)
            if 'existing_instructor' in form_data and len(form_data['existing_instructor']) > 0:
                instructor_ids.append(form_data['existing_instructor'])
            print "instructor ids: ", instructor_ids
            # with returned ids, we then go and add entries to relational table
            self.instructors.add_class_instructors(class_id, instructor_ids)
            return class_id


    def update(self, form_data):
        # update class
        query = "UPDATE classes SET name=:name, duration=:duration, email_text=:email_text, date=:date, updated_at=NOW(), race_verbiage=:race_verbiage, cvpm_verbiage=cvpm_verbiage WHERE id=:id"
        values = {
            "name": form_data['name'],
            "duration": form_data['duration'],
            "email_text": form_data['email_text'],
            "date": form_data['date'],
            "race_verbiage": form_data['race_verbiage'],
            "cvpm_verbiage": form_data['cvpm_verbiage'],
            "id": form_data['id']
        }
        class_id = form_data['id']
        self.postgresql.query_db(query, values)
        # collect all instructors to be removed, pass to instructors remove function
        remove_instructors = {}
        # collect all instructors to be updated, pass to instructors update function
        update_instructors = {}
        # collect all instructors to be added, pass to add instructors function
        add_instructor = []
        for key in form_data:
            if key.startswith('remove'):
                id = key[6:]
                # print id
                remove_instructors[id] = form_data[key]
            elif key.startswith('instructor') and len(form_data[key]) > 0:
                id = key[10:]
                # print id
                update_instructors[id] = form_data[key]
            elif key.startswith('new_instructor') and len(form_data[key]) > 0:
                add_instructor.append(form_data[key])
        print "instructors to add: ", add_instructor
        print "instructors to update: ", update_instructors
        print "instructors to remove: ", remove_instructors
        print "existing instructors to add: ", form_data['existing_instructor']
        self.instructors.delete_class_relationship(class_id, remove_instructors)
        added_instructors = self.instructors.add(add_instructor, class_id)
        if len(form_data['existing_instructor']) > 0:
            added_instructors.append(form_data['existing_instructor'])
        self.instructors.add_class_instructors(class_id, added_instructors)
        self.instructors.update(update_instructors)


    def findAll(self):
        query = "SELECT * FROM classes";
        classes = self.postgresql.query_db(query)
        return classes


    def findIncomplete(self):
        query = "SELECT * FROM classes WHERE status=:status"
        values = {
            "status": "incomplete"
        }
        incomplete_classes = self.postgresql.query_db(query, values)
        return incomplete_classes


    def findOne(self, class_id):
        query = "SELECT * FROM classes WHERE id=:class_id";
        values = {
            "class_id": class_id
        }
        one_class = self.postgresql.query_db(query, values)
        return one_class[0]

    def required_miutes(self, class_id):
        query = "SELECT duration FROM classes WHERE id=:id"
        values = {
            "id": class_id
        }
        duration = self.postgresql.query_db(query, values)
        return duration
