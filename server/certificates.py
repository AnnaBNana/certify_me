import csv
import os
from server.psqlconnection import PSQLConnector
from server.attendees import Attendees
from werkzeug import secure_filename
from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
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
        self.stylesheet = getSampleStyleSheet()
        self.attendees = Attendees(app)


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
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            attendee_info = self.attendees.add_attendees(reader, class_data['class_id'])
        return attendee_info


    def generate(self):
        layout = self.read_layout()
        layout_data = self.parse_layout(layout)
        pdf = self.make_pdf(layout_data)
        self.merge_pdfs()


    def get_pdf_data(self, class_id):
        pass


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
        fp.close()
        return layout

    def parse_layout(self, layout):
        #put pdf miner layout parsing here, return obj coords for text placement
        coords = {}
        top_coords = prev_top_coords = bottom_coords = keyword = prev_keyword = None
        flowable_dict = {}
        found = flag = False
        layout_bounds = layout.bbox
        keywords = ['student', 'seminar', 'instructor', 'race_verbiage', 'date', 'cvmp_verbiage']
        for lt_obj in layout:
            # print "object: ", lt_obj
            # print "lt obj object name: ", lt_obj.__class__.__name__
            # print "lt obj bbox: ", lt_obj.bbox
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                # print "lt obj text: ", lt_obj.get_text()
                # if any of the keywords from above list are found, save coords in key value pair and save keyword, set found bool to true for use in setting bounding boxes
                for k in keywords:
                    if k in lt_obj.get_text().lower():
                        coords[k] = lt_obj.bbox
                        found = True
                        keyword = k
                # algorithm to set bounding boxes for report lab flowables:
                # if the line is not blank and we have not yet found a keyword
                if lt_obj.get_text() != "\t\n" and found == False:
                    # create a top set of coords that include the bounding box of the most recent text containing line
                    top_coords = lt_obj.bbox
                # if our keyword has been found and line is not blank, end bounding box, add new item to our dict of coords, and reset booleans and start looking for next keyword
                if lt_obj.get_text() != "\t\n" and flag == True:
                    bottom_coords = lt_obj.bbox
                    flowable_dict[prev_keyword] = {
                        'top': prev_top_coords,
                        'bottom': bottom_coords
                    }
                    found = flag = False
                    if keyword != prev_keyword:
                        found = True
                    else:
                        top_coords = lt_obj.bbox
                # this means we have found a keyword and we now should track keyword, and mark that item is found, and we are still looking for our bottom bound
                if found == True:
                    flag = True
                    found = False
                    prev_top_coords = top_coords
                    top_coords = lt_obj.bbox
                    prev_keyword = keyword
                # temp_coords = lt_obj.bbox
            elif isinstance(lt_obj, LTFigure):
                self.parse_layout(lt_obj)
        # if the last line contains a keyword, our flag boolean will be left open.  close it using arbitrary params based on doc dimensions, which will always be letter size
        if flag == True:
            flowable_dict[keyword] = {
                'top': prev_top_coords,
                'bottom': (0,0,0,70)
            }
        # package data we will need to use later in the process
        layout_data = {
            'coords': coords,
            'flowable_bounds': flowable_dict,
            'layout_bounds': layout_bounds}
        return layout_data


    def make_pdf(self, layout_data):
        style = self.stylesheet['BodyText']
        style.alignment = TA_CENTER
        coords = layout_data['coords']
        flowable_bounds = layout_data['flowable_bounds']
        layout_bounds = layout_data['layout_bounds']
        w1 = layout_bounds[2] - 160
        new_file = self.app.config['UPLOAD_FOLDER'] + "temp.pdf"
        packet = StringIO.StringIO()
        cv = Canvas(packet, pagesize=letter)
        font = "Helvetica"
        for key in coords:
            topx1 = flowable_bounds[key]['top'][0]
            topy1 = flowable_bounds[key]['top'][1]
            bottomx2 = flowable_bounds[key]['bottom'][2]
            bottomy2 = flowable_bounds[key]['bottom'][3]
            h1 = topy1 - bottomy2
            style.fontName = "Helvetica"
            if key == 'instructor':
                s = "God"
                style.fontSize = 18
            elif key =='student':
                s = "Anna Propas"
                style.fontSize = 36
                style.fontName = 'Helvetica-BoldOblique'
            elif key == 'seminar':
                s = "Anna Propas Is Awesome"
                style.fontSize = 18
            elif key == "race_verbiage":
                s = "some RACE text that is really long so that word wrap will have to start working.  let's see how this looks is it long enough, should have done some lorem ipsum or something, this sucks."
                style.fontSize = 8
                style.fontName = 'Helvetica-Oblique'
            elif key == "cvmp_verbiage":
                s = "some CVMP text"
                style.fontSize = 8
                style.fontName = 'Helvetica-Oblique'
            elif key == "date":
                new = "June 20, 2016"
                s = "has attended the following webinar on " + new
                style.fontSize = 14
            cv.setFillColor("white")
            white_out_w = coords[key][2] - coords[key][0]
            white_out_h = coords[key][3] - coords[key][1]
            cv.rect(coords[key][0], coords[key][1], white_out_w, white_out_h, stroke=0, fill=1)
            cv.setFillColor("black")
            p = Paragraph(s, style)
            w2,h2 = p.wrap(layout_bounds[2] - 160, h1)
            if w2<=w1 and h2<=h1:
                p.drawOn(cv, 80, topy1 - (h1/2))
            else:
                raise ValueError, "not enough room"
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
