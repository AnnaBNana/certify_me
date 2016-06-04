from flask import Flask, jsonify, session
from server.psqlconnection import PSQLConnector
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')
bcrypt = Bcrypt(app)

class Users(object):
    def add(self, form_data):
        # check if email already exists in the database
        email_validation_query = "SELECT * FROM users WHERE (email = :email)"
        email_validation_values = {
            "email": form_data['email']
        }
        validate = postgresql.query_db(email_validation_query, email_validation_values)
        #validation check should return an empty array if email is unique
        if validate == []:
            password = form_data['password']
            hashed_password = bcrypt.generate_password_hash(password)
            if form_data['permission'] == "super-admin":
                client_id = 7
            else:
                client_id = form_data['client']
            # print client_id
            query_users = "INSERT INTO users (email, password, created_at, permission, name, client_id) VALUES (:email, :password, NOW(), :permission, :name, :client_id) RETURNING id"
            values_users = {
                "email": form_data['email'],
                "password": hashed_password,
                "permission": form_data['permission'],
                "name": form_data['name'],
                "client_id": client_id
            }
            id = postgresql.query_db(query_users, values_users)
            # print id
            res_dict = {'id': id}
            return jsonify(res_dict)
        else:
            error = {'error': "user email already in database, please enter unique email"}
            return jsonify(error)
    def login(self, form_data):
        if not form_data['password'] or not form_data['email']:
            error = {'error': 'please fill out login form'}
            return error
        else:
            user = self.findOneFromEmail(form_data['email'])
        #did db query return
            if user == []:
                error = {'error': 'user cannot be found in the database'}
                return error
            else:
                if bcrypt.check_password_hash(user[0]['password'], form_data['password']):
                    session['user_id'] = user[0]['id']
                    session['client_id'] = user[0]['client_id']
                    session['permission'] = user[0]['permission']
                    session['logged'] = True
                    success = {"success": user[0]['id'], "permission": user[0]['permission']}
                    return success
                else:
                    error = {"error": "email or password did not match an existing user in the database"}
                    return error
    def findAll(self):
        return "all users"
    def findOne(self):
        return "one user"
    def findOneFromEmail(self, email):
        query = "SELECT * FROM users WHERE email=:email"
        value = {
            "email": email
        }
        return postgresql.query_db(query, value)
