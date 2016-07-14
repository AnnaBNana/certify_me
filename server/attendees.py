from server.psqlconnection import PSQLConnector
from server.classes import Classes


class Attendees(object):
    def __init__(self, app):
        self.classes = Classes(app)
        self.postgresql = PSQLConnector(app, 'CertifyMe')

    def add_attendees(self, contents, class_id):
        # we are missing validation for csv files to ensure they are formatted as expected
        query = "INSERT INTO attendees (name, email, created_at) VALUES (:name, :email, NOW()) RETURNING id"
        attendee_info = []
        i = 0
        min_check = {}
        rel_info = []
        for row in contents:
            print "row: ", row
            if i == 2:
                header = row
            elif i > 2:
                if row:
                    if row[1] not in min_check:
                        row_data = {
                            'name': row[0],
                            'email': row[1],
                            'min': row[2]
                        }
                        attendee_info.append(row_data)
                    if row[1] in min_check:
                        min_check[row[1]] += int(row[2])
                    else:
                        min_check[row[1]] = int(row[2])
            i += 1
        for info in attendee_info:
            if info['email'] in min_check:
                info['min'] = min_check[info['email']]
            values = {
                'name': info['name'],
                'email': info['email']
            }
            at_id = self.postgresql.query_db(query, values)
            info = {
                "id": at_id,
                "minutes": info['min']
            }
            rel_info.append(info)
        self.add_attended_classes(rel_info, class_id)
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

    def get_cert_data(self, class_id):
        query = "SELECT a.name AS name, a.email AS email, ac.minutes AS minutes, c.name AS class_name, c.duration AS duration, c.email_text AS email_text, c.date AS class_date, c.race_verbiage AS race_verbiage, c.cvpm_verbiage AS cvpm_verbiage, c.race_course_num AS course_num FROM attendees AS a LEFT JOIN  attended_classes AS ac ON a.id=ac.attendee_id LEFT JOIN classes AS c ON ac.class_id=c.id WHERE c.id=:class_id"
        values = {
            "class_id": class_id
        }
        cert_data = self.postgresql.query_db(query, values)
        return cert_data

    def find_all_in_class(self, class_id):
        query = "SELECT a.id AS attendee_id, a.name AS name, a.email AS email, ac.minutes AS minutes, c.duration AS duration, c.email_text AS email_text FROM attendees AS a LEFT JOIN attended_classes AS ac ON a.id=ac.attendee_id LEFT JOIN classes AS c ON ac.class_id=c.id WHERE c.id=:class_id AND ac.minutes >= c.duration"
        values = {
            "class_id": class_id
        }
        students = self.postgresql.query_db(query, values)
        return students
