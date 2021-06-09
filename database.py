from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


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


class Pin(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    game = relationship(Game)
    color = db.Column(db.String, db.ForeignKey('pincolor.color'))
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)


class PinColor(db.Model):
    color = db.Column(db.String, primary_key=True)


db.create_all()
