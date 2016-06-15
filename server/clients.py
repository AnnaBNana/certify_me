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
        # social_media_1 : facebook
        # social_media_2 : twitter
        # social_media_3 : instagram
        client_query = "INSERT INTO clients (email, name, title, business_id, social_media_1, social_media_2, social_media_3, created_at) VALUES (:email, :name, :title, :business_id, :facebook, :twitter, :instagram, NOW()) RETURNING id;"
        client_values = {
            "email": form_data['email'],
            "name": form_data['name'],
            "title": form_data['title'],
            "business_id": biz_id,
            "facebook": form_data['facebook'],
            "twitter": form_data['twitter'],
            "instagram": form_data['instagram']
        }
        client_id = self.postgresql.query_db(client_query, client_values)
        session['client_id'] = client_id
        print "client id: ", client_id
        return str(client_id)
    def update(self, form_data):
        query = "UPDATE clients SET email=:email, name=:name, title=:title, social_media_1=:fb, social_media_2=:twit, social_media_3=:inst, updated_at=NOW() WHERE id=:id"
        values = {
            "email": form_data['email'],
            "name": form_data['name'],
            "title": form_data['title'],
            "fb": form_data['facebook'],
            "twit": form_data['twitter'],
            "inst": form_data['instagram'],
            "id": form_data['client_id']
        }
        self.postgresql.query_db(query, values)
    def findAll(self):
        query = "SELECT clients.id AS id, clients.name AS client_name, clients.email AS email, businesses.name AS business_name FROM clients LEFT JOIN businesses ON clients.business_id=businesses.id WHERE clients.id!=7"
        clients = self.postgresql.query_db(query)
        return clients
    def findOne(self, id):
        query = "SELECT c.id AS client_id, email, c.name AS client_name, title, social_media_1, social_media_2, social_media_3, b.id AS business_id, b.name AS business_name, street, city, state, zip, website FROM clients c, businesses b WHERE c.id=:id"
        values = {
            "id": id
        }
        client = self.postgresql.query_db(query, values)
        return client[0]
