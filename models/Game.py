from database import db
from sqlalchemy.orm import relationship

from models.User import User


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User)
    turns = db.Column(db.Integer)
    cheat_mode = db.Column(db.Boolean)
    duplicate_color = db.Column(db.Boolean)
    number_of_colors = db.Column(db.Integer)
    number_of_positions = db.Column(db.Integer)