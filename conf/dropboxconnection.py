import dropbox
import os

class Dropbox(object):
    #######################################################################
    # CONSTRUCTOR METHODS, INITIALIZE ATTRIBUTES FOR CONNECTION TO DROPBOX
    #######################################################################
    def __init__(self, app):
        #dropbox settings
        self.app = app
        self.access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        self.client = dropbox.client.DropboxClient(self.access_token)
        self.app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'csv'])
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'

    #######################################################################
    # STORE ALL GENERATED PDFS TO DROPBOX
    #######################################################################

    def save_all(self, biz, seminar):
        name = biz['name']
        date = str(seminar['date'])
        for f in os.listdir(self.app.config['UPLOAD_FOLDER']):
            print "line 25 in drop connection: file:", f
            message = {}
            if os.path.isfile(self.app.config['UPLOAD_FOLDER'] + f):
                print "line 28 in drop connection: is file"
                client_path = "/" + name.replace(" ", "") + "/" + date + "/"
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], f)
                if f.endswith('.csv'):
                    fo = open(self.app.config['UPLOAD_FOLDER'] + f, 'r')
                elif f.endswith('.pdf'):
                    fo = open(self.app.config['UPLOAD_FOLDER'] + f, 'rb')
                    if f == biz['pdf_url']:
                        client_path = "/" + name.replace(" ", "") + "/"
                else:
                    continue
                if self.client.put_file(client_path + f, fo, overwrite=True):
                    os.remove(self.app.config['UPLOAD_FOLDER'] + f)
                    message = {'success': 'success'}
        print "list dir after removal of files:", os.listdir(self.app.config['UPLOAD_FOLDER'])
        return message

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
