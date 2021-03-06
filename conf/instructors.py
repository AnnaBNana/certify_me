from conf.psqlconnection import PSQLConnector

class Instructors(object):
    def __init__(self, app, db):
        self.postgresql = PSQLConnector(app, db)

    def add(self, instructor_list, class_id):
        #instructor name is unique constriant, which we are not handling here! should do upsert
        instructor_query = "INSERT INTO instructors (name, created_at)\
                            VALUES (:name, NOW())\
                            ON CONFLICT (name)\
                            DO UPDATE SET updated_at=NOW()\
                            RETURNING id"
        all_instructor_ids = []
        for name in instructor_list:
            instructor = {"name": name}
            instructor_id = self.postgresql.query_db(instructor_query, instructor)
            all_instructor_ids.append(instructor_id)
        return all_instructor_ids

    def add_class_instructors(self, class_id, instructor_ids):
        instructor_query = "INSERT INTO class_instructor (instructor_id, class_id)\
                            VALUES (:instructor_id, :class_id)\
                            RETURNING instructor_id"
        for id in instructor_ids:
            instructor = {
                "instructor_id": id,
                "class_id": class_id
            }
            self.postgresql.query_db(instructor_query, instructor)

    def findAll(self, business_id):
        if business_id == 23:
            query = "SELECT * FROM instructors"
            instructors = self.postgresql.query_db(query)
        else:
            query = "SELECT i.id, i.name FROM instructors AS i LEFT JOIN class_instructor AS ci ON i.id=ci.instructor_id LEFT JOIN classes AS c ON ci.class_id=c.id WHERE business_id=:business_id"
            values = {
                "business_id": business_id
            }
            instructors = self.postgresql.query_db(query, values)
        return instructors

    def find_all_class_instructors(self, class_id):
        query = "SELECT * FROM class_instructor AS ci LEFT JOIN instructors AS i ON ci.instructor_id=i.id WHERE ci.class_id=:id"
        values = {
            "id": class_id
        }
        class_instructors = self.postgresql.query_db(query, values)
        # print class_instructors
        return class_instructors

    def find_all_other(self, class_id):
        # print "class id: ", class_id
        query = "SELECT * FROM class_instructor LEFT JOIN instructors ON class_instructor.instructor_id=instructors.id WHERE class_instructor.class_id!=:id"
        values = {
            "id": class_id
        }
        all_other_instructors = self.postgresql.query_db(query, values)
        # print "all other instructors: ", all_other_instructors
        return all_other_instructors

    def delete_class_relationship(self, class_id, instructor_ids):
        query = "DELETE FROM class_instructor WHERE instructor_id=:instructor_id AND class_id=:class_id"
        for id in instructor_ids:
            instructor = {
                "instructor_id": id,
                "class_id": class_id
            }
            self.postgresql.query_db(query, instructor)

    def update(self, instructors):
        query = "UPDATE instructors SET name=:name WHERE id=:id"
        for id in instructors:
            values = {
                "id": id,
                "name": instructors[id]
            }
            self.postgresql.query_db(query, values)
