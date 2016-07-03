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
            print i
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
        print "check attendee_info ", attendee_info
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
