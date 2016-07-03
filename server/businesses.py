from server.psqlconnection import PSQLConnector

class Businesses(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')


    def add(self, form_data):
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
        return biz_id


    def update(self, form_data):
        print form_data
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
