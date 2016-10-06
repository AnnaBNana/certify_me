from conf.psqlconnection import PSQLConnector
from conf.classes import Classes


class Attendees(object):
    def __init__(self, app, db):
        self.classes = Classes(app, db)
        self.postgresql = PSQLConnector(app, db)

    def add_attendees(self, contents, class_id):
        # we are missing validation for csv files to ensure they are formatted as expected
        select_query = "SELECT id FROM attendees WHERE email=:email"
        insert_query = "INSERT INTO attendees (name, email, status, created_at) VALUES (:name, :email, :status, NOW()) RETURNING id"
        update_query = "UPDATE attendees SET name=:name, status=:status, updated_at=NOW() WHERE id=:id"
        attendee_info = []
        i = 0
        min_check = {}
        rel_info = []
        header_marker = None;
        for row in contents:
            # print "row: ", row
            if row:
                # print "inside conditional", row
                if row[1] == "Email":
                    header_marker = i
                if header_marker and i > header_marker and row[1]:
                    if row[1] not in min_check:
                        row_data = {
                            'name': row[0],
                            'email': row[1],
                            'min': row[2]
                        }
                        attendee_info.append(row_data)
                    if row[1] in min_check:
                        print "email:", row[1]
                        min_check[row[1]] += int(row[2])
                    else:
                        print "email:", row[1]
                        min_check[row[1]] = int(row[2])
                i += 1
        for info in attendee_info:
            if info['email'] in min_check:
                info['min'] = min_check[info['email']]
            # query db to see if email is in db
            stat = self.postgresql.query_db(select_query, {'email':info['email']})
            # if email in db update row
            if stat:
                print "attendees.py line 48: this user already exists in db: ", info['email'], stat[0]['id']
                values = {
                    'name': info['name'],
                    'status': 'in_db',
                    'id': stat[0]['id']
                }
                query = update_query
                self.postgresql.query_db(query, values)
                student_id = stat[0]['id']
            # else insert
            else:
                values = {
                    'name': info['name'],
                    'email': info['email'],
                    'status': 'in_db'
                }
                query = insert_query
                student_id = self.postgresql.query_db(query, values)
            info = {
                "id": student_id,
                "minutes": info['min']
            }
            rel_info.append(info)
        self.add_attended_classes(rel_info, class_id)
        return attendee_info

    def add_attended_classes(self, attendee_info, class_id):
        insert_query = "INSERT INTO attended_classes (attendee_id, class_id, minutes) VALUES (:attendee_id, :class_id, :minutes) RETURNING attendee_id"
        select_query = "SELECT * FROM attended_classes WHERE attendee_id = :attendee_id AND class_id = :class_id"
        for info in attendee_info:

            select_values = {
                "attendee_id": info['id'],
                "class_id": class_id
            }
            exists = self.postgresql.query_db(select_query, select_values)
            #handle errors if data given is not an integer, should be esp. careful w/ minutes
            if not exists:
                insert_values = {
                    "attendee_id": info['id'],
                    "class_id": class_id,
                    "minutes": info['minutes']
                }
                self.postgresql.query_db(insert_query, insert_values)

    def get_cert_data(self, class_id):
        query = "SELECT a.id AS attendee_id, a.name AS name, a.email AS email, ac.minutes AS minutes, c.name AS class_name, c.duration AS duration, c.email_text AS email_text, c.date AS class_date, c.race_verbiage AS race_verbiage, c.cvpm_verbiage AS cvpm_verbiage, c.race_course_num AS course_num FROM attendees AS a LEFT JOIN  attended_classes AS ac ON a.id=ac.attendee_id LEFT JOIN classes AS c ON ac.class_id=c.id WHERE c.id=:class_id AND a.status=:status"
        values = {
            "class_id": class_id,
            "status": "in_db"
        }
        cert_data = self.postgresql.query_db(query, values)
        return cert_data

    def findOne(self, id):
        query = "SELECT * FROM attendees WHERE id=:id"
        values = {
            "id": id
        }
        student = self.postgresql.query_db(query, values)
        return student[0]

    def find_all_in_class(self, class_id):
        query = "SELECT a.id AS attendee_id, a.name AS name, a.email AS email, a.status AS status, ac.minutes AS minutes, c.duration AS duration, c.email_text AS email_text FROM attendees AS a LEFT JOIN attended_classes AS ac ON a.id=ac.attendee_id LEFT JOIN classes AS c ON ac.class_id=c.id WHERE c.id=:class_id AND ac.minutes >= c.duration AND a.email!= '' ORDER BY a.created_at DESC"
        values = {
            "class_id": class_id
        }
        students = self.postgresql.query_db(query, values)
        return students

    def update_status(self, students, status):
        query = "UPDATE attendees SET status=:status WHERE id=:id"
        for student in students:
            values = {
                'status': status,
                'id': student['attendee_id']
            }
            self.postgresql.query_db(query, values)
