import re
from inspect import currentframe, getframeinfo

from flask import session

from conf.psqlconnection import PSQLConnector
from conf.instructors import Instructors


class Classes(object):
    def __init__(self, app, db):
        self.postgresql = PSQLConnector(app, db)
        self.instructors = Instructors(app, db)

    def add(self, form_data):
        session
        print "form data", form_data
        valid = True
        messages = {}
        data = {}
        course_regex = re.compile(r'^(\d+)-(\d+)')
        match_obj = re.match(course_regex, form_data['course_num'])
        instructor_list = []
        for k, v in form_data.iteritems():
            #check every key to see if it begins with new instructor
            if k.startswith('new_instructor'):
                #if it does push value to a list
                instructor_list.append(v)
        if len(form_data['name']) < 6:
            messages['name_error'] = "name must be 6 characters or more"
            valid = False
        if not match_obj:
            messages['course_num_error'] = "Expected digits-digits format, please check course number"
        if not form_data['duration'].isdigit():
            messages['duration_error']= "Please enter a whole number"
            valid = False
        if len(form_data['date']) < 10:
            messages['date_error']= "Please enter correct date format"
            valid = False
        if form_data['existing_instructor'] == "" and len(instructor_list) < 1:
            messages['instructor_error']= "Please choose existing instructor or add at least one new instructor"
            valid = False
        #make this requirement longer in deployment, length requirement shortened for testing
        if len(form_data['email_text']) < 4:
            messages['email_error']= "Email must be at least 4 characters in length"
            valid = False
        if len(form_data['race_verbiage']) < 4:
            print "race validation fail"
            messages['race_verbiage']= "Race verbiage must be at least 4 characters in length"
            valid = False
        if valid:
            query = "INSERT INTO classes (name, duration, business_id, email_text, date, created_at, race_verbiage, cvpm_verbiage, race_course_num) VALUES (:name, :duration, :business_id, :email_text, :date, NOW(), :race_verbiage, :cvpm_verbiage, :race_course_num) RETURNING id"
            values = {
                "name": form_data['name'],
                "duration": form_data['duration'],
                "business_id": session['business_id'],
                "email_text": form_data['email_text'],
                "date": form_data['date'],
                "race_verbiage": form_data['race_verbiage'],
                "cvpm_verbiage": form_data['cvpm_verbiage'],
                "race_course_num": form_data['course_num']
            }
            # add class, return id
            class_id = self.postgresql.query_db(query, values)
            print class_id
            # add instructor names from list items to db as a group, return ids
            instructor_ids = self.instructors.add(instructor_list, class_id)
            if 'existing_instructor' in form_data and len(form_data['existing_instructor']) > 0:
                instructor_ids.append(form_data['existing_instructor'])
            # with returned ids, we then go and add entries to relational table
            self.instructors.add_class_instructors(class_id, instructor_ids)
            messages['id'] = class_id
        return messages

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
        self.instructors.delete_class_relationship(class_id, remove_instructors)
        added_instructors = self.instructors.add(add_instructor, class_id)
        if len(form_data['existing_instructor']) > 0:
            added_instructors.append(form_data['existing_instructor'])
        self.instructors.add_class_instructors(class_id, added_instructors)
        self.instructors.update(update_instructors)

    def findAll(self, business_id):
        if session['permission'] == "super-admin":
            query = "SELECT * FROM classes";
            classes = self.postgresql.query_db(query)
        else:
            query = "SELECT * FROM classes WHERE business_id=:biz_id"
            values = {
                "biz_id": business_id
            }
            classes = self.postgresql.query_db(query, values)
        return classes

    def find_all_for_biz(self, business_id):
        query = "SELECT * FROM classes WHERE business_id=:biz_id"
        values = {
            "biz_id": business_id
        }
        classes = self.postgresql.query_db(query, values)
        return classes

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
        return self.postgresql.query_db(query, values)

    def update_email(self, email_text, class_id):
        query = "UPDATE classes SET email_text=:email_text WHERE id=:class_id"
        values = {
            "email_text": email_text,
            "class_id": class_id
        }
        self.postgresql.query_db(query, values)

    def get_email_text(self, class_id):
        query = "SELECT email_text FROM classes WHERE id=:class_id"
        values = {
            "class_id": class_id
        }
        email_text = self.postgresql.query_db(query, values)
        return email_text[0]['email_text']
