from flask import Flask, session
from server.psqlconnection import PSQLConnector

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')

class Instructors(object):
    def add(self, instructor_list, class_id):
        instructor_query = "INSERT INTO instructors (name, created_at) VALUES (:name, NOW()) RETURNING id"
        #iterate through list of instructor names, running an insert statement for each instructor
        #this is faster than a dynamically generated multi-row insert, and it does not require multi-threading
        all_instructor_ids = []
        for name in instructor_list:
            instructor = {"name": name}
            instructor_id = postgresql.query_db(instructor_query, instructor)
            all_instructor_ids.append(instructor_id)
        print all_instructor_ids
        return all_instructor_ids
    def add_class_instructors(self, class_id, instructor_ids):
        instructor_query = "INSERT INTO class_instructor (instructor_id, class_id) VALUES (:instructor_id, :class_id) RETURNING instructor_id"
        for id in instructor_ids:
            instructor = {
                "instructor_id": id,
                "class_id": class_id
            }
            postgresql.query_db(instructor_query, instructor)
    def findAll(self):
        query = "SELECT * FROM instructors"
        instructors = postgresql.query_db(query)
        return instructors
    def find_all_class_instructors(self, class_id):
        query = "SELECT * FROM class_instructor LEFT JOIN instructors ON class_instructor.instructor_id=instructors.id WHERE class_instructor.class_id=:id"
        values = {
            "id": class_id
        }
        class_instructors = postgresql.query_db(query, values)
        # print class_instructors
        return class_instructors
    def find_all_other(self, class_id):
        # print "class id: ", class_id
        query = "SELECT * FROM class_instructor LEFT JOIN instructors ON class_instructor.instructor_id=instructors.id WHERE class_instructor.class_id!=:id"
        values = {
            "id": class_id
        }
        all_other_instructors = postgresql.query_db(query, values)
        # print "all other instructors: ", all_other_instructors
        return all_other_instructors