from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SetupDatabase:
    def __init__(self, db):
        self.db = db

    def create_database(self):
        try:
            open('database.db')

        except IOError:
            self.db.create_all()
