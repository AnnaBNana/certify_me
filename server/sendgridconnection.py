import sendgrid
import os


class SendgridConnection(object):
    def __init__(self, app):
        self.app = app
        self.access_token = os.environ.get('SENDGRID_ACCESS_TOKEN')
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        sg = sendgrid.SendGridAPIClient(apikey=self.access_token)

    def send(self):
        pass
