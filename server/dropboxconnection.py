import dropbox
import os

class Dropbox(object):
    def __init__(self, app):
        #dropbox settings
        self.app = app
        access_token = os.environ.get('ACCESS_TOKEN')
        self.client = dropbox.client.DropboxClient(access_token)
        self.app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'csv'])
    def upload(self, files_data):
        # since this takes so long, give client option to upload files to dropbox after the rest of the operations are complete
        upload_loc = "./static/uploads/"
        f0 = open(upload_loc + filearray[0], 'r')
        self.client.put_file("/" + filearray[0], f0)
        f1 = open(upload_loc + filearray[1], 'rb')
        self.client.put_file("/" + filearray[1], f1)
        # after all operations complete, remove files from local file storage

        # something like this: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.filename))
    def get_file(self, file_name):
        out = open(file_name, 'wb')
        with self.client.get_file(file_name) as f:
            out.write(f.read())
