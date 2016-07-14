from flask import session
import re
from server.psqlconnection import PSQLConnector
from flask.ext.bcrypt import Bcrypt

class Users(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')
        self.bcrypt = Bcrypt(app)
        self.email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
    def add(self, form_data):
        message = {}
        # check if email already exists in the database
        email_dupe_query = "SELECT * FROM users WHERE (email = :email)"
        email_dupe_values = {
            "email": form_data['email']
        }
        email_dupe = self.postgresql.query_db(email_dupe_query, email_dupe_values)
        #validation check should return an empty array if email is unique
        if not email_dupe:
            password = form_data['password']
            hashed_password = self.bcrypt.generate_password_hash(password)
            valid = True
            if len(form_data['name']) < 5:
                message['name_error'] = 'name must be 4 characters or more'
                valid = False
            if not self.email_regex.match(form_data['email']):
                message['email_error'] = 'email entered is not a valid email format'
                valid = False
            if len(password) < 8:
                message['password_error'] = 'password must be 8 characters or more'
                valid = False
            if not valid:
                return message
            if form_data['permission'] == "super-admin":
                business_id = 23
            else:
                business_id = form_data['business']
            query_users = "INSERT INTO users (email, password, created_at, permission, name, business_id) VALUES (:email, :password, NOW(), :permission, :name, :business_id) RETURNING id"
            values_users = {
                "email": form_data['email'],
                "password": hashed_password,
                "permission": form_data['permission'],
                "name": form_data['name'],
                "business_id": business_id
            }
            id = self.postgresql.query_db(query_users, values_users)
            # print id
            message['id'] = id
        else:
            message['dupe_error'] = "user email already in database, please enter unique email"
        return message

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
                if self.bcrypt.check_password_hash(user[0]['password'], form_data['password']):
                    session['user_id'] = user[0]['id']
                    session['business_id'] = user[0]['business_id']
                    session['permission'] = user[0]['permission']
                    session['logged'] = True
                    success = {"success": user[0]['id'], "permission": user[0]['permission']}
                    return success
                else:
                    error = {"error": "email or password did not match an existing user in the database"}
                    return error
    def update(self, form_data):
        if 'permission' not in form_data:
            permission = "super-admin"
        else:
            permission = form_data['permission']
        query = "UPDATE users SET name=:name, email=:email, permission=:permission, updated_at=NOW() WHERE id=:id"
        values = {
            "name": form_data['name'],
            "email": form_data['email'],
            "permission": permission,
            "id": form_data['id']
        }
        self.postgresql.query_db(query, values)

    def update_password(self, form_data, user_id):
        message = {}
        user = self.findOne(user_id)
        if len(form_data['newpword']) < 8:
            message['validation_err'] = "new password must be at least 8 characters long"
        elif not self.bcrypt.check_password_hash(user['password'], form_data['oldpword']):
            message['validation_err'] = "password entered is incorrect"
        else:
            password = form_data['newpword']
            hashed_password = self.bcrypt.generate_password_hash(password)
            query = "UPDATE users SET password=:password WHERE id=:id"
            values = {
                'password': hashed_password,
                'id': user_id
            }
            self.postgresql.query_db(query, values)
        return message

    def findAll(self):
        query = "SELECT * FROM users"
        users = self.postgresql.query_db(query)
        return users

    def findOne(self, id):
        query = "SELECT * FROM users WHERE id=:id"
        values = {
            "id": id
        }
        user = self.postgresql.query_db(query, values)
        return user[0]

    def findOneFromEmail(self, email):
        query = "SELECT * FROM users WHERE email=:email"
        value = {
            "email": email
        }
        return self.postgresql.query_db(query, value)

    def destroy(self, id):
        query = "DELETE FROM users WHERE id=:id"
        values = {
            "id":id
        }
        self.postgresql.query_db(query, values)
