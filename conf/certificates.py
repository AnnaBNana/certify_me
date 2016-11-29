import csv
import datetime
import os
import re
from inspect import currentframe, getframeinfo

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.converter import PDFPageAggregator
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import StringIO
from werkzeug import secure_filename


from conf.attendees import Attendees
from conf.psqlconnection import PSQLConnector

class Certificates(object):
    def __init__(self, app, db):
        self.app = app
        self.postgresql = PSQLConnector(app, db)
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        self.stylesheet = getSampleStyleSheet()
        self.attendees = Attendees(app, db)
        self.alphanum_regex = re.compile(r'\w+')

    def save_files(self, files):
        filearray = []
        for all_file in files:
            new_file = files[all_file]
            filename = secure_filename(new_file.filename)
            new_file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
            filearray.append(new_file.filename)
        return filearray

    def parseCSV(self, class_data):
        with open(self.app.config['UPLOAD_FOLDER'] + class_data['csv_file'], 'rU') as csvfile:
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            attendee_info = self.attendees.add_attendees(reader, class_data['class_id'])
        return attendee_info

    def generate(self, pdf_data):
        layout = self.read_layout(pdf_data['template_pdf'])
        # print "certificates line 57 layout from read layout function:", layout
        layout_data = self.parse_layout(layout)
        #get student data, execute the next two functions for each person in class
        students = pdf_data['students']
        print "{}, line {}".format(getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno), "students", students
        for student in students:
            print "{}, line {}".format(getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno), "student", student
            if student['email']:
                print "{}, line {}".format(getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno), "student email", student['email']
                messages = self.make_pdf(layout_data, student, pdf_data['inst'])
                # print "certificates line 67 messages:", messages
                valid = True
                for message in messages:
                    if 'placement_error' in message:
                        # print "certificates line 71 placement error:", message
                        valid = False
                if valid:
                    self.merge_pdfs(student, pdf_data['template_pdf'])
            else:
                messages = [
                    {'email_error': 'please provide valid email for each student'}
                ]
                break
        return messages

    def read_layout(self, template_pdf):
        #put pdf miner code for preping layout for parsing
        fp = open(self.app.config['UPLOAD_FOLDER'] + template_pdf, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            self.parse_layout(layout)
        fp.close()
        # print "certificates line 98, finished reading layout:", layout
        return layout

    def parse_layout(self, layout):
        #put pdf miner layout parsing here, return obj coords for text placement
        coords = {}
        top_coords = prev_top_coords = bottom_coords = keyword = prev_keyword = None
        flowable_dict = {}
        found = flag = False
        layout_bounds = layout.bbox
        keywords = ['student', 'seminar', 'instructor', 'race_verbiage', 'date', 'cvpm_verbiage', 'class_id']
        # print "certificates line 97 layout:", layout
        for lt_obj in layout:
            # print "certificates line 99 object: ", lt_obj
            # print "certificates line 100 lt obj object name: ", lt_obj.__class__.__name__
            # print "certificates line 101 lt obj bbox: ", lt_obj.bbox
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                # print "lt obj text: ", lt_obj.get_text()
                # if any of the keywords from above list are found, save coords in key value pair and save keyword, set found bool to true for use in setting bounding boxes
                if self.alphanum_regex.search(lt_obj.get_text()):
                    for k in keywords:
                        if k in lt_obj.get_text().lower():
                            coords[k] = lt_obj.bbox
                            found = True
                            keyword = k
                # algorithm to set bounding boxes for report lab flowables:
                # if the line is not blank and we have not yet found a keyword
                if self.alphanum_regex.search(lt_obj.get_text()) and not found:
                    # create a top set of coords that include the bounding box of the most recent text containing line
                    top_coords = lt_obj.bbox
                 # if our keyword has been found and line is not blank, end bounding box, add new item to our dict of coords, and reset booleans and start looking for next keyword
                if self.alphanum_regex.search(lt_obj.get_text()) and flag:
                    bottom_coords = lt_obj.bbox
                    flowable_dict[prev_keyword] = {
                        'top': prev_top_coords,
                        'bottom': bottom_coords
                    }
                    # print "coords dict in order found:", flowable_dict
                    found = flag = False
                    if keyword != prev_keyword:
                        found = True
                    else:
                        top_coords = lt_obj.bbox
                # this means we have found a keyword and we now should track keyword, and mark that item is found, and we are still looking for our bottom bound
                if found:
                    flag = True
                    found = False
                    prev_top_coords = top_coords
                    top_coords = lt_obj.bbox
                    prev_keyword = keyword
                temp_coords = lt_obj.bbox
            elif isinstance(lt_obj, LTFigure):
                self.parse_layout(lt_obj)
        # # if the last line contains a keyword, our flag boolean will be left open.  close it using arbitrary params based on doc dimensions, which will always be letter size
        # print "flag", flag
        if flag:
            layoutx2 = layout_bounds[2]
            # print "certificates line 141 layout x2:", layoutx2
            flowable_dict[keyword] = {
                'top': prev_top_coords,
                'bottom': (0,0,layoutx2,80)
            }
        # package data we will need to use later in the process
        layout_data = {
            'coords': coords,
            'flowable_bounds': flowable_dict,
            'layout_bounds': layout_bounds}
        # print "layout data certificates line 151:", layout_data
        return layout_data

    def make_pdf(self, layout_data, student, instructors):
        messages = []
        style = self.stylesheet['BodyText']
        style.alignment = TA_CENTER
        coords = layout_data['coords']
        flowable_bounds = layout_data['flowable_bounds']
        layout_bounds = layout_data['layout_bounds']
        w1 = layout_bounds[2] - 160
        new_file = self.app.config['UPLOAD_FOLDER'] + "temp.pdf"
        # print "new file, certificates line 177", new_file
        packet = StringIO.StringIO()
        cv = Canvas(packet, pagesize=letter)
        font = "Helvetica"
        for key in coords:
            topy1 = flowable_bounds[key]['top'][1]
            bottomy2 = flowable_bounds[key]['bottom'][3]
            h1 = topy1 - bottomy2
            w = layout_bounds[2] - layout_bounds[0]
            style.fontName = "Helvetica"
            if key == 'instructor':
                s = str()
                for i in instructors:
                    s += i['name'] + "\n"
                style.fontSize = 18
            elif key =='student':
                s = student['name']
                style.fontSize = 28
                style.fontName = 'Helvetica-BoldOblique'
            elif key == 'seminar':
                s = student['class_name']
                style.fontSize = 18
            elif key == 'class_id':
                s = student['course_num']
                style.fontSize = 14
            elif key == "race_verbiage":
                s = student['race_verbiage']
                style.fontSize = 8
                style.fontName = 'Helvetica-Oblique'
            elif key == "cvpm_verbiage":
                s = student['cvpm_verbiage']
                style.fontSize = 6
                style.fontName = 'Helvetica-Oblique'
            elif key == "date":
                d = datetime.datetime.strptime(student['class_date'], '%Y-%m-%d')
                d = d.strftime('%B %d,%Y')
                s = "has attended the following on " + str(d)
                style.fontSize = 14
            cv.setFillColor("white")
            # cover up keyword
            white_out_w = coords[key][2] - coords[key][0]
            white_out_h = coords[key][3] - coords[key][1]
            cv.rect(coords[key][0], coords[key][1], white_out_w, white_out_h, stroke=0, fill=1)
            cv.setFillColor("black")
            # alot space for wrapable text and add text to that space
            p = Paragraph(s, style)
            w2,h2 = p.wrap(layout_bounds[2] - 160, h1)
            if w2<=w1 and h2<=h1:
                if key == 'race_verbiage' or key == 'cvpm_verbiage':
                    p.drawOn(cv, 80, bottomy2)
                else:
                    p.drawOn(cv, 80, topy1 - (h1/2))
                messages.append({'success': 'everything is good'})
            else:
                messages.append({'placement_error': 'there is not enough room for ' + str(key) + '. Increase space available for ' + str(key) + ' and try again.'})
        cv.save()
        packet.seek(0)
        with open(new_file,'wb') as fp:
            fp.write(packet.getvalue())
        return messages


    def merge_pdfs(self, student, template_pdf):
        name = student['name']
        name = name.replace(" ", "")
        # basic merge of two docs
        pdf1 = PdfFileReader(file(self.app.config['UPLOAD_FOLDER'] + template_pdf, "rb"))
        # create new doc for each attendee, merge this doc into base
        pdf2 = PdfFileReader(file(self.app.config['UPLOAD_FOLDER'] + 'temp.pdf', "rb"))
        output = PdfFileWriter()
        page = pdf1.getPage(0)
        page.mergePage(pdf2.getPage(0))
        output.addPage(page)
        student_name = name
        #3rd pdf is final version
        outputStream = file(self.app.config['UPLOAD_FOLDER'] + name + '.pdf', 'wb')
        output.write(outputStream)
        outputStream.close()
        os.remove(self.app.config['UPLOAD_FOLDER'] + 'temp.pdf')
