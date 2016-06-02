from flask import Flask
from server.psqlconnection import PSQLConnector

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')

class Classes(object):
    def register(self, form_data):
        print "form data", form_data
        return "id"
    def findAll(self):
        return "all classes"
    def findOne(self):
        return "one class"
