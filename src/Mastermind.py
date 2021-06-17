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

    def guess_the_code(self, guessed_colors):
        result = {
            "in_but_not_correct": 0,
            "correct": 0,
        }

        # Check if pins are in exactly the right spot
        code = self.Game.code
        i = 0
        for guessed_color in guessed_colors:
            if guessed_color is not None and code[i] == guessed_color:
                result['correct'] += 1
                code[i] = None
            i += 1

        # Check if remaining pins are not in the right spot but have the right colour
        i = 0
        for guessed_color in guessed_colors:
            if guessed_color is not None:
                j = 0
                for color_code in code:
                    if color_code is not None and color_code == guessed_color:
                        result['in_but_not_correct'] += 1
                        code[i] = None
                    j += 1
            i += 1
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
