from flask import Flask
from server.psqlconnection import PSQLConnector
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')
bcrypt = Bcrypt(app)

class Users(object):
    def register(self, form_data):
        print "form data ", form_data
        password = form_data['password']
        hashed_password = bcrypt.generate_password_hash(password)
        print "hashed password ", hashed_password
        query_users = "INSERT INTO users (email, password, created_at, permission, name) VALUES (:email, :password, NOW(), :permission, :name)"
        values_users = {
            "email": form_data['email'],
            "password": hashed_password,
            "permission": form_data['permission'],
            "name": form_data['name']
        }
        id = postgresql.query_db(query_users, values_users);
        return id
    def login(self):
        return "id"
    def findAll(self):
        return "all users"
    def findOne(self):
        return "one user"
