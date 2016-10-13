import sendgrid
from sendgrid.helpers.mail import *
import os
import base64

class SendgridConnection(object):

    #######################################################################
    # CONSTRUCTOR METHODS, INITIALIZE ATTRIBUTES FOR CONNECTION TO SENDGRID
    #######################################################################

    def __init__(self, app):
        self.app = app
        self.access_token = os.environ.get('SENDGRID_ACCESS_TOKEN')
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        self.sg = sendgrid.SendGridAPIClient(apikey=self.access_token)

    #######################################################################
    # SEND EMAIL METHODS
    #######################################################################

    def send(self, business_data, class_data, student_data):
        stripped_name = student_data['name'].replace(" ", "")
        pdf_name = stripped_name + ".pdf"
        file_path = self.app.config['UPLOAD_FOLDER'] + stripped_name + ".pdf"
        with open(file_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        mail = Mail()
        mail.set_from(Email(business_data['email']))
        personalization = Personalization()
        personalization.add_to(Email(student_data['email']))
        mail.add_personalization(personalization)
        mail.set_subject("Certificate for: " + class_data['name'])
        mail.add_content(Content('text/html', "<p>" + student_data['name'] + ", </p>" + class_data['email_text']))
        attachment = Attachment()
        attachment.set_content(encoded_string)
        attachment.set_type("application/pdf")
        attachment.set_filename(pdf_name)
        attachment.set_disposition("attachment")
        attachment.set_content_id("Certificate")
        mail.add_attachment(attachment)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        # print "(sendgrid line 34)email response:", vars(response), dir(response)
        return response
