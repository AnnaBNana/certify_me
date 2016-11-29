from conf.psqlconnection import PSQLConnector
from conf.classes import Classes
from inspect import currentframe, getframeinfo


class Attendees(object):
    #######################################################################
    # CONSTUCTORS
    #######################################################################
    def __init__(self, app, db):
        self.classes = Classes(app, db)
        self.postgresql = PSQLConnector(app, db)

    #######################################################################
    # SELECT METHODS
    #######################################################################

    def findOne(self, id):
        query = "SELECT * FROM attendees WHERE id=:id"
        values = {
            "id": id
        }
        student = self.postgresql.query_db(query, values)
        return student[0]

    def get_cert_data(self, class_id):
        query = "SELECT a.id AS attendee_id, a.name AS name, a.email AS email, ac.minutes AS minutes, c.name AS class_name, c.duration AS duration, c.email_text AS email_text, c.date AS class_date, c.race_verbiage AS race_verbiage, c.cvpm_verbiage AS cvpm_verbiage, c.race_course_num AS course_num\
        FROM attendees AS a\
        LEFT JOIN  attended_classes AS ac\
        ON a.id=ac.attendee_id\
        LEFT JOIN classes AS c\
        ON ac.class_id=c.id\
        WHERE c.id=:class_id AND a.status=:status"
        values = {
            "class_id": class_id,
            "status": "in_db"
        }
        cert_data = self.postgresql.query_db(query, values)
        return cert_data

    def find_all_in_class(self, class_id):
        query = "SELECT a.id AS attendee_id, a.name AS name, a.email AS email, a.status AS status, ac.minutes AS minutes, c.duration AS duration, c.email_text AS email_text\
        FROM attendees AS a\
        LEFT JOIN attended_classes AS ac\
        ON a.id=ac.attendee_id\
        LEFT JOIN classes AS c\
        ON ac.class_id=c.id\
        WHERE c.id=:class_id AND ac.minutes >= c.duration AND a.email!= ''\
        ORDER BY a.created_at DESC"
        values = {
            "class_id": class_id
        }
        students = self.postgresql.query_db(query, values)
        return students

    #######################################################################
    # INSERT METHODS
    #######################################################################

    def add_attendees(self, contents, class_id):
        upsert_query = "INSERT INTO attendees (name, email, status, created_at)\
                        VALUES (:name, :email, :status, NOW())\
                        ON CONFLICT (email)\
                        DO UPDATE SET name=:name, status=:status, updated_at=NOW()\
                        RETURNING id"
        attendee_info = []
        i = 0
        min_check = {}
        rel_info = []
        header_marker = None;
        for row in contents:
            if row:
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
            #COULD ADD ATTENDEE AT THIS STAGE INSTEAD OF BULK AT THE END
            if info['email'] in min_check:
                info['min'] = min_check[info['email']]
            values = {
                'name': info['name'],
                'email': info['email'],
                'status': 'in_db'
            }
            #UPSERT STUDENT ACCORDING TO DATA EXTRACTED FROM CSV, EMAIL IS UNIQUE CONSTRAINT
            student_id = self.postgresql.query_db(upsert_query, values)
            ac_info = {
                "id": student_id,
                "minutes": info['min']
            }
            rel_info.append(ac_info)
        self.add_attended_classes(rel_info, class_id)
        return attendee_info

    def add_attended_classes(self, attendee_info, class_id):
        upsert_query = "INSERT into attended_classes (attendee_id, class_id, minutes)\
                        VALUES (:attendee_id, :class_id, :minutes)\
                        ON CONFLICT (attendee_id, class_id)\
                        DO UPDATE SET minutes = :minutes\
                        RETURNING attendee_id"
        for info in attendee_info:
            values = {
                "attendee_id": info['id'],
                "class_id": class_id,
                "minutes": info['minutes']
            }
            self.postgresql.query_db(upsert_query, values)

    #######################################################################
    # UPDATE METHODS
    #######################################################################

    def update_status(self, students, status):
        query = "UPDATE attendees SET status=:status WHERE id=:id"
        for student in students:
            values = {
                'status': status,
                'id': student['attendee_id']
            }
            self.postgresql.query_db(query, values)
