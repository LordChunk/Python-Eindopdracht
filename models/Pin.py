from sqlalchemy.orm import relationship

from database import db
from models.Game import Game


class Pin(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    game = relationship(Game)
    color = db.Column(db.String, db.ForeignKey('pincolor.color'))
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)