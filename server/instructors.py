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
    def findAll(self):
        query = "SELECT * FROM instructors"
        instructors = postgresql.query_db(query)
        return instructors
