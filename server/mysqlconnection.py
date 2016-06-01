from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

class MySQLConnection(object):
    def __init__(self, app, db):
        config = {
                'host': 'localhost',
                'database': db,
                'user': 'apropas',
                'password': 'root',
                'port': 'localhost'
        }
        DATABASE_URI = "postgresql://{}:{}@127.0.0.1:{}/{}".format(config['user'], config['password'], config['port'], config['database'])
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        print app.config
        self.db = SQLAlchemy(app)
    def query_db(self, query, data=None):
        result = self.db.session.execute(text(query), data)
        if query[0:6].lower() == 'select':
            list_result = [dict(r) for r in result]
            return list_result
        elif query[0:6].lower() == 'insert':
            self.db.session.commit()
            return result.lastrowid
        else:
            self.db.session.commit()
def MySQLConnector(app, db):
    return MySQLConnection(app, db)
