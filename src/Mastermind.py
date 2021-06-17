import random

from database import db
from models.Color import Color
from models.Game import Game
from models.Pin import Pin


class Mastermind:

    def __init__(self, Game):
        self.Game = Game

    def make_code(self):
        secret_code = []
        for x in range(self.Game.number_of_colors):
            color = self.get_random_color()

            if not self.Game.duplicate_color:
                while color in secret_code:
                    color = self.get_random_color()

            secret_code.append(color)

        Game.code = secret_code
        return secret_code

    def get_random_color(self):
        return Color(random.randint(0, self.Game.number_of_colors - 1))

    def get_all_results(self):
        pins = Pin.query.filter_by(game_id=self.Game.id).all()

        all_results = []

        for x in range(10):
            all_results.append(guess_the_code())

    def guess_the_code(self, guessed_code):
        result = {
            "in_but_not_correct": 0,
            "correct": 0,
        }

        # ToDo: fix bug with duplicate colors
        for guessed_colors in range(len(guessed_code)):
            if self.Game.code[guessed_colors] == guessed_code[guessed_colors]:
                result["correct"] += 1
            else:
                for color in range(len(self.Game.code)):
                    if self.Game.code[color] == guessed_code[guessed_colors]:
                        if guessed_colors == color:
                            result["correct"] += 1
                        else:
                            result["in_but_not_correct"] += 1
                        break
        return result

    def add_new_pin_row(self, color_row):
        i = 0
        for pinColor in color_row:
            if pinColor is not None:
                pin = Pin(
                    game_id=self.Game.id,
                    color=str(pinColor),
                    x=i,
                    y=self.Game.turns
                )
                db.session.add(pin)
            i += 1

        self.Game.turns += 1
        db.session.commit()

    def did_player_win(self, result):
        if Game.number_of_positions == result["correct"]:
            return True

        return False
