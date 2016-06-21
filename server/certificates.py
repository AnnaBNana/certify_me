import csv
import os
from server.psqlconnection import PSQLConnector
from werkzeug import secure_filename
from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.converter import PDFPageAggregator


class Certificates(object):
    def __init__(self, app):
        self.app = app
        self.postgresql = PSQLConnector(app, 'CertifyMe')
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'


    def upload_files(self, files):
        filearray = []
        upload_loc = "./static/uploads/"
        for all_file in files:
            new_file = files[all_file]
            filename = secure_filename(new_file.filename)
            new_file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
            filearray.append(upload_loc + new_file.filename)
        return filearray

    def parseCSV(self, class_data):
        with open(class_data['csv_file'], 'rU') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            attendee_info = self.add_attendees(reader, class_data['class_id'])
        return attendee_info


    def add_attendees(self, contents, class_id):
        # we are missing validation for csv files to ensure they are formatted as expected
        print contents
        query = "INSERT INTO attendees (name, email, created_at) VALUES (:name, :email, NOW()) RETURNING id"
        attendee_info = []
        i = 0
        for row in contents:
            if i == 2:
                header = row
            elif i > 2:
                if row:
                    #handle some errors, row[0] should be alpha only, row[1] should be email, return error otherwise
                    values = {
                        'name': row[0],
                        'email': row[1]
                    }
                    at_id = self.postgresql.query_db(query, values)
                    # we can validate minutes here. generate PDF only if we pass time limit.  we will have to query the class table to get req'd mins
                    info = {
                        "id": at_id,
                        "minutes": row[2]
                    }
                    attendee_info.append(info)
            i += 1
        print attendee_info, class_id
        self.add_attended_classes(attendee_info, class_id)
        return attendee_info


    def add_attended_classes(self, attendee_info, class_id):
        query = "INSERT INTO attended_classes (attendee_id, class_id, minutes) VALUES (:attendee_id, :class_id, :minutes) RETURNING attendee_id"
        for info in attendee_info:
            #handle errors if data given is not an integer, should be esp. careful w/ minutes
            values = {
                "attendee_id": info['id'],
                "class_id": class_id,
                "minutes": info['minutes']
            }
            self.postgresql.query_db(query, values)


    def handle_pdfs(self):
        layout = self.read_layout()
        coords = self.parse_layout(layout)
        pdf = self.make_pdf(coords)
        print coords
        self.merge_pdfs()


    def read_layout(self):
        #put pdf miner code for preping layout for parsing
        fp = open(self.app.config['UPLOAD_FOLDER'] + 'template.pdf', 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        device = PDFDevice(rsrcmgr)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            self.parse_layout(layout)
            # print "layout: ", layout
        fp.close()
        return layout

    def parse_layout(self, layout):
        #put pdf miner layout parsing here, return obj coords for text placement
        coords = {}
        for lt_obj in layout:
            print "object: ", lt_obj
            print "lt obj class, name", lt_obj.__class__.__name__
            print "lt obj bbox", lt_obj.bbox
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                print "lt obj text: ", lt_obj.get_text()
                if "student" in lt_obj.get_text():
                    coords['name'] = lt_obj.bbox
                if "webinar" in lt_obj.get_text():
                    coords['class_name'] = lt_obj.bbox
                if "Instructor" in lt_obj.get_text():
                    coords['instructor_name'] = lt_obj.bbox
                if "verbiage" in lt_obj.get_text():
                    coords['race'] = lt_obj.bbox
            elif isinstance(lt_obj, LTFigure):
                self.parse_layout(lt_obj)
        # print "coords: ", coords
        return coords


    def make_pdf(self, coords):
        name = "student name"
        instructor_name = "instructor of class name"
        class_name = "name of this class"
        race = "race verbiage for this class"
        new_file = self.app.config['UPLOAD_FOLDER'] + "temp.pdf"
        packet = StringIO.StringIO()
        cv=canvas.Canvas(packet, pagesize=letter)
        center_y = 4.25 * inch
        for key in coords:
            if key == 'instructor_name':
                s = "instructor of class name"
                cv.setFont("Helvetica", 18)
            elif key =='name':
                s = "student name"
                cv.setFont("Helvetica", 48)
            elif key == 'class_name':
                s = "name of class"
                cv.setFont("Helvetica", 36)
            elif key == "race":
                s = "some RACE text"
                cv.setFont("Helvetica", 10)
            cv.setFillColor("coral")
            w = coords[key][2] - coords[key][0]
            h = coords[key][3] - coords[key][1]
            cv.rect(coords[key][0], coords[key][1], w, h, stroke=0, fill=1)
            cv.setFillColor("black")
            cv.setStrokeColor("black")
            cv.drawCentredString(center_y, coords[key][1], s)
        cv.save()
        packet.seek(0)
        with open(new_file,'wb') as fp:
            fp.write(packet.getvalue())


    def merge_pdfs(self):
        # basic merge of two docs
        pdf1 = PdfFileReader(file(self.app.config['UPLOAD_FOLDER'] + 'template.pdf', "rb"))
        # create new doc for each attendee, merge this doc into base
        pdf2 = PdfFileReader(file(self.app.config['UPLOAD_FOLDER'] + 'temp.pdf', "rb"))
        output = PdfFileWriter()
        page = pdf1.getPage(0)
        page.mergePage(pdf2.getPage(0))
        output.addPage(page)
        student_name = "placeholder"
        #3rd pdf is final version
        outputStream = file(self.app.config['UPLOAD_FOLDER'] + student_name + '.pdf', 'wb')
        output.write(outputStream)
        outputStream.close()
        os.remove(self.app.config['UPLOAD_FOLDER'] + 'temp.pdf')
