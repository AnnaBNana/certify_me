import sendgrid
import os
from sendgrid.helpers.mail import *

class SendgridConnection(object):
    def __init__(self, app):
        self.app = app
        self.access_token = os.environ.get('SENDGRID_ACCESS_TOKEN')
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        self.sg = sendgrid.SendGridAPIClient(apikey=self.access_token)

    def send(self):
        from_email = Email("apropas@gmail.com")
        subject = "Hello World from the SendGrid Python Library"
        to_email = Email("apropas@codingdojo.com")
        content = Content("text/plain", "some text here www.facebook.com")
        mail = Mail(from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        # print student_ids
