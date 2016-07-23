from flask import session

from conf.psqlconnection import PSQLConnector
from conf.businesses import Businesses


class Clients(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')
        self.businesses = Businesses(app)

    def add(self, id, form_data):
        valid = True
        message = {}
        if len(form_data['name']) < 5:
            message['name_error'] = "name must be 4 characters or more"
            valid = False
        if len(form_data['title']) < 3:
            message['title_error'] = "title must be 2 characters or more"
            valid = False
        if valid:
            client_query = "INSERT INTO clients (name, title, business_id, created_at) VALUES (:name, :title, :business_id, NOW()) RETURNING id;"
            client_values = {
                "name": form_data['name'],
                "title": form_data['title'],
                "business_id": id
            }
            self.postgresql.query_db(client_query, client_values)
            message['success'] = "client added to database"
        return message

    def update(self, form_data):
        # print form_data
        query = "UPDATE clients SET name=:name, title=:title, updated_at=NOW() WHERE id=:id"
        client_ids = []
        for client_info in form_data:
            # print client_info
            if client_info.startswith('id'):
                client_ids.append(form_data[client_info])
        print client_ids
        for id in client_ids:
            values = {
                "name": form_data['name' + id],
                "title": form_data['title' + id],
                "id": id
            }
            print "values: ", values
            self.postgresql.query_db(query, values)

    def findAll(self):
        query = "SELECT * FROM clients"
        clients = self.postgresql.query_db(query)
        return clients

    def find_biz_owners(self, biz_id):
        query = "SELECT * FROM clients WHERE business_id=:biz_id"
        values = {
            "biz_id": biz_id
        }
        clients = self.postgresql.query_db(query, values)
        return clients

    def destroy(self, id):
        query = "DELETE FROM clients WHERE id=:id"
        values = {
            "id": id
        }
        self.postgresql.query_db(query, values)
