import dropbox
import os

class Dropbox(object):
    def __init__(self, app):
        #dropbox settings
        self.app = app
        self.access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        self.client = dropbox.client.DropboxClient(self.access_token)
        self.app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'csv'])
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        # self.dropbox_path = "/AAVSBCertificates"

    def save_all(self, biz, seminar):
        name = biz['name']
        date = str(seminar['date'])
        for f in os.listdir(self.app.config['UPLOAD_FOLDER']):
            client_path = "/" + name.replace(" ", "") + "/" + date + "/"
            if f.endswith('.csv'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + f, 'r')
            elif f.endswith('.pdf'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + f, 'rb')
                if f == biz['pdf_url']:
                    client_path = "/" + name.replace(" ", "") + "/"
            else:
                continue
            if self.client.put_file(client_path + f, fo, overwrite=True):
                message = {'success': 'success'}
            else:
                message = {}
        # after all operations complete, remove files from local file storage
        print "list dir before removal of files:", os.listdir(self.app.config['UPLOAD_FOLDER'])
        for file_name in os.listdir(self.app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print "list dir after removal of files:", os.listdir(self.app.config['UPLOAD_FOLDER'])
        return message

    def get_file(self, file_name, business):
        name = business['name'].replace(" ", "")
        file_path = "/" + name + "/" + file_name
        myfile = self.client.get_file(file_path)
        out = open(self.app.config['UPLOAD_FOLDER'] + file_name, 'wb')
        out.write(myfile.read())
        out.close()
