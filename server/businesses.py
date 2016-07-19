from server.psqlconnection import PSQLConnector
import re

class Businesses(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')
        self.street_addr_regex = re.compile(r'^\d+\s[a-zA-Z]+')
        self.zip_addr_regex = re.compile(r'^[0-9]{5}')
        self.email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

    def add(self, form_data):
        valid = True
        message = {}
        data = {}
        if len(form_data['business_name']) < 4:
            message['biz_name_error'] = "business name must be 4 charcters or more"
            valid = False
        if len(form_data['street_addr']) < 7:
            message['street_addr_error'] = "street address must be 6 characters or more"
            valid = False
        elif not self.street_addr_regex.match(form_data['street_addr']):
            message['street_addr_error'] = "street address not formatted correctly"
            valid = False
        if len(form_data['city_addr']) < 3:
            message['city_addr_error'] = "city name must be 3 characters or longer"
            valid = False
        if len(form_data['state_addr']) != 2:
            message['state_addr_error'] = "please select a state"
            valid = False
        if not self.zip_addr_regex.match(form_data['zip_addr']):
            message['zip_addr_error'] = "zipcode is not valid, should be only numeric and contain 5 digits"
            valid = False
        if not self.email_regex.match(form_data['email']):
            message['email_error'] = "email format is not valid"
            valid = False
        if valid:
            biz_query = "INSERT INTO businesses (name, street, city, state, zip, website, email, social_media_1, social_media_2, social_media_3, created_at) VALUES (:name, :street, :city, :state, :zip, :website, :email, :facebook, :twitter, :instagram, NOW()) RETURNING id;"
            biz_values = {
                "name": form_data['business_name'],
                "street": form_data['street_addr'],
                "city": form_data['city_addr'],
                "state": form_data['state_addr'],
                "zip": form_data['zip_addr'],
                "website": form_data['url'],
                "email": form_data['email'],
                "facebook": form_data['facebook'],
                "twitter": form_data['twitter'],
                "instagram": form_data['instagram']
            }
            biz_id = self.postgresql.query_db(biz_query, biz_values)
            data['biz_id'] = biz_id
        else:
            data['message'] = message
        return data

    def update(self, form_data):
        # print form_data
        query = "UPDATE businesses SET name=:name, street=:street, city=:city, state=:state, zip=:zip, website=:website, social_media_1=:facebook, social_media_2=:twitter, social_media_3=:instagram, updated_at=NOW() WHERE id=:id"
        values = {
            "name": form_data['business_name'],
            "street": form_data['street_addr'],
            "city": form_data['city_addr'],
            "state": form_data['state_addr'],
            "zip": form_data['zip_addr'],
            "website": form_data['website'],
            "facebook": form_data['facebook'],
            "twitter": form_data['twitter'],
            "instagram": form_data['instagram'],
            "id": form_data['business_id']
        }
        self.postgresql.query_db(query, values)

    def findOne(self, biz_id):
        query = "SELECT * FROM businesses WHERE id=:biz_id"
        values = {
            "biz_id": biz_id
        }
        biz_info = self.postgresql.query_db(query, values)
        return biz_info[0]

    def findAll(self):
        query = "SELECT * FROM businesses WHERE name!=:name"
        values = {
            "name": "dummy"
        }
        businesses = self.postgresql.query_db(query, values)
        return businesses

    def add_pdf_url(self, business_data):
        query = "UPDATE businesses SET pdf_url=:pdf_url, updated_at=NOW() WHERE id=:id"
        values = {
            "pdf_url": business_data['pdf'],
            "id": business_data['id']
        }
        self.postgresql.query_db(query, values)

    def check_pdf_url(self, business_id):
        query = "SELECT pdf_url FROM businesses WHERE id=:business_id"
        values = {
            "business_id": business_id
        }
        url = self.postgresql.query_db(query, values)
        return url

    def add_dropbox_api_key(self, key, client_id):
        with open('venv/bin/activate', 'a') as file:
            export_string = "export " + str(client_id) + "ACCESS_KEY = " + str(key) + "\n"
            file.write(str(export_string))
