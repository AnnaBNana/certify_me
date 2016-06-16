import csv
from server.psqlconnection import PSQLConnector

class Certificates(object):
    def __init__(self, app):
        self.postgresql = PSQLConnector(app, 'CertifyMe')


    def add(self):
        pass


    def findAll(self):
        pass


    def parse(self, csv_file_one):
        print csv_file_one
        with open(csv_file_one, 'rU') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            header = reader.next()
            print header
            # for column in header:
            #     print "i am a value", column
            i = 0
            for row in reader:
                if i == 2:
                    print "this should be header: ", i
                    i += 1
                for j in i:
                    print j


    def destroy(self):
        pass
