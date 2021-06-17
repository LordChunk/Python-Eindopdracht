from database import db
from sqlalchemy.orm import relationship
from models.Color import Color
from models.User import User
import random


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User)
    turns = db.Column(db.Integer)
    cheat_mode = db.Column(db.Boolean)
    duplicate_color = db.Column(db.Boolean)
    number_of_colors = db.Column(db.Integer)
    number_of_positions = db.Column(db.Integer)
    code = db.Column(db.PickleType, nullable=False)
    won = db.Column(db.Boolean, nullable=True)

    def make_code(self):
        secret_code = []
        for x in range(self.amountOfColorsInCode):
            color = self.get_random_color()

            if not self.duplicate_colors:
                while color in secret_code:
                    color = self.get_random_color()

            secret_code.append(color)

        return secret_code

    def get_random_color(self):
        return Color(random.randint(0, self.number_of_colors_in_code - 1))

    def guess_the_code(self, guessed_code):
        return True
