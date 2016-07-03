from flask import session
from server.psqlconnection import PSQLConnector
from server.businesses import Businesses

class Clients(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')
        self.businesses = Businesses(app)


    def add(self, form_data):
        print "form data", form_data
        if 'existing_biz' in form_data:
            biz_id = form_data['existing_biz']
        else:
            biz_id = self.businesses.add(form_data)
        print "biz id: ", biz_id
        client_query = "INSERT INTO clients (name, title, business_id, created_at) VALUES (:name, :title, :business_id, NOW()) RETURNING id;"
        client_values = {
            "name": form_data['name'],
            "title": form_data['title'],
            "business_id": biz_id
        }
        client_id = self.postgresql.query_db(client_query, client_values)
        session['client_id'] = client_id
        print "client id: ", client_id
        return str(client_id)


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
