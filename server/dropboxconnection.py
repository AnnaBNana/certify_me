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
    def upload(self, filearray):
        # since this takes so long, give client option to upload files to dropbox after the rest of the operations are complete
        for f in filearray:
            if f.endswith('.csv'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + filearray[0], 'r')
            elif f.endswith('.pdf'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + filearray[1], 'rb')
            self.client.put_file("/" + f, fo)
        # after all operations complete, remove files from local file storage
        # something like this: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.filename))


    def get_file(self, file_name):
        myfile = self.client.get_file(file_name)
        out = open(self.app.config['UPLOAD_FOLDER'] + file_name, 'wb')
        out.write(myfile.read())
        out.close()
