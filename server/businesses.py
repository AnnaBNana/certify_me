from flask import Flask
from server.psqlconnection import PSQLConnector

app = Flask(__name__)
postgresql = PSQLConnector(app, 'CertifyMe')

class Businesses(object):
    def add(self, form_data):
        biz_query = "INSERT INTO businesses (name, street, city, state, zip, website, created_at) VALUES (:name, :street, :city, :state, :zip, :website, NOW()) RETURNING id;"
        biz_values = {
            "name": form_data['business_name'],
            "street": form_data['street_addr'],
            "city": form_data['city_addr'],
            "state": form_data['state_addr'],
            "zip": form_data['zip_addr'],
            "website": form_data['url']
        }
        biz_id = postgresql.query_db(biz_query, biz_values)
        return biz_id
    def update(self, form_data):
        print form_data
        query = "UPDATE businesses SET name=:name, street=:street, city=:city, state=:state, zip=:zip, website=:website, updated_at=NOW() WHERE id=:id"
        values = {
            "name": form_data['business_name'],
            "street": form_data['street_addr'],
            "city": form_data['city_addr'],
            "state": form_data['state_addr'],
            "zip": form_data['zip_addr'],
            "website": form_data['website'],
            "id": form_data['business_id']
        }
        postgresql.query_db(query, values)
    def findOne(self, biz_id):
        query = "SELECT * FROM businesses WHERE id=:id"
        values = {
            "id": biz_id
        }
        biz_info = postgresql.query_db(query, values)
        return biz_info
    def findAll(self):
        query = "SELECT * FROM businesses"
        businesses = postgresql.query_db(query)
        return businesses
