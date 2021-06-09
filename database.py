from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class SetupDatabase:
    def __init__(self, db):
        self.db = db

    def create_database(self):
        try:
            open('database.db')

        except IOError:
            self.db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User)
    turns = db.Column(db.Integer)
    cheat_mode = db.Column(db.Boolean)
    duplicate_color = db.Column(db.Boolean)
    number_of_colors = db.Column(db.Integer)
    number_of_positions = db.Column(db.Integer)


class PinColor(db.Model):
    __tablename__ = 'pincolor'
    color = db.Column(db.String, primary_key=True)


class Pin(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    game = relationship(Game)
    color = db.Column(db.String, db.ForeignKey('pincolor.color'))
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)

