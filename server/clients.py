from flask import Flask
from server.psqlconnection import PSQLConnector

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')

class Clients(object):
    def register(self, form_data):
        print "form data", form_data
        biz_query = "INSERT INTO businesses (name, street, city, state, zip, website, created_at) VALUES (:name, :street, :city, :state, :zip, :website, NOW()) RETURNING id"
        biz_values = {
            "name": form_data['business_name'],
            "street": form_data['street_addr'],
            "city": form_data['city_addr'],
            "state": form_data['state_addr'],
            "zip": form_data['zip_addr'],
            "website": form_data['url']
        }
        biz_id = postgresql.query_db(biz_query, biz_values);
        print "biz id: ", biz_id
        #social_media_1 : facebook
        #social_media_2 : twitter
        #social_media_3 : instagram
        client_query = "INSERT INTO clients (email, name, title, business_id, social_media_1, social_media_2, social_media_3, created_at) VALUES (:email, :name, :title, :business_id, :facebook, :twitter, :instagram, NOW())"
        client_values = {
            "email": form_data['email'],
            "name": form_data['name'],
            "title": form_data['title'],
            "business_id": biz_id,
            "facebook": form_data['facebook'],
            "twitter": form_data['twitter'],
            "instagram": form_data['instagram']
        }
        client_id = postgresql.query_db(client_query, client_values);
        return str(biz_id), str(client_id)
    def findAll(self):
        return "all clients"
    def findOne(self):
        return "one client"
