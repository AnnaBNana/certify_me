import dropbox
import os
from inspect import currentframe, getframeinfo

class Dropbox(object):
    #######################################################################
    # CONSTRUCTOR METHODS, INITIALIZE ATTRIBUTES FOR CONNECTION TO DROPBOX
    #######################################################################
    def __init__(self, app):
        self.app = app
        self.access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        self.client = dropbox.client.DropboxClient(self.access_token)
        self.app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'csv'])
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'

    #######################################################################
    # SAVE TO DROPBOX
    #######################################################################

    def save_all(self, biz, seminar):
        data = {
            'name': biz['name'],
            'date': str(seminar['date']),
            'pdf_url': biz['pdf_url']
        }
        message = {}
        for f in os.listdir(self.app.config['UPLOAD_FOLDER']):
            if self.upload(data, f):
                self.delete_file(f)
                message = {'success': 'success'}
        return message

    def upload(self, data, file_name):
        if os.path.isfile(self.app.config['UPLOAD_FOLDER'] + file_name):
            client_path = "/" + data['name'].replace(" ", "").encode('utf-8') + "/" + data['date'] + "/"
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], file_name)
            if file_name.endswith('.csv'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + file_name, 'r')
            elif file_name.endswith('.pdf'):
                fo = open(self.app.config['UPLOAD_FOLDER'] + file_name, 'rb')
                if file_name == data['pdf_url']:
                    client_path = "/" + data['name'].replace(" ", "") + "/"
            if self.client.put_file(client_path + file_name, fo, overwrite=True):
                return True

    #######################################################################
    # REMOVE FILE FROM LOCAL STORAGE
    #######################################################################

    def delete_file(self, file_name):
        os.remove(self.app.config['UPLOAD_FOLDER'] + file_name)

    #######################################################################
    # RETRIEVE NEEDED FILES, SUCH AS BUSINESS TEMPLATE PDF, FROM DROPBOX
    #######################################################################

    def get_file(self, file_name, business):
        name = business['name'].replace(" ", "")
        file_path = "/" + name + "/" + file_name
        try:
            myfile = self.client.get_file(file_path)
            out = open(self.app.config['UPLOAD_FOLDER'] + file_name, 'wb')
            out.write(myfile.read())
            out.close()
            message = {'success': 'success'}
        except:
            message = {'file_error': 'file was not found in your dropbox folder, please upload a new template'}
        return message
