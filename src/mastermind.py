import random
from models.Color import Color


class MasterMind:
    number_of_colors_in_code = 4
    duplicate_colors = False
    secret_code = []

    def __init__(self, number_of_colors_in_code, duplicate_colors):
        self.number_of_colors_in_code = number_of_colors_in_code
        self.duplicate_colors = duplicate_colors

    def make_code(self):
        for color in range(self.amountOfColorsInCode):
            color = self.get_random_color()

            if not self.duplicate_colors:
                while color in self.secret_code:
                    color = self.get_random_color()

            self.secret_code.append()

    def get_random_color(self):
        return self.Color(random.randint(0, self.number_of_colors_in_code - 1))
