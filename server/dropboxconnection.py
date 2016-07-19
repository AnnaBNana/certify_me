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
        client_path = "/" + name.replace(" ", "") + "/" + date
        for f in filearray:
            if f.endswith('.csv'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + filearray[0], 'r')
            elif f.endswith('.pdf'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + filearray[1], 'rb')
                if f == biz['pdf_url']:
                    client_path = "/" + name.replace(" ", "")
            self.client.put_file(client_path + f, fo, mode=dropbox.files.WriteMode.overwrite)
        # after all operations complete, remove files from local file storage
        for file_name in os.listdir(self.app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def get_file(self, file_name):
        print self.client.account_info()
        myfile = self.client.get_file(file_name)
        out = open(self.app.config['UPLOAD_FOLDER'] + file_name, 'wb')
        out.write(myfile.read())
        out.close()
