import random
from models.Color import Color
from models.Game import Game


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

    def get_random_color(self):
        return Color(random.randint(0, self.Game.number_of_colors - 1))

    def guess_the_code(self, guessed_code):
        return True


