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

        # get a code that has the length of the number of positions possible
        for x in range(self.Game.number_of_positions):

            # pick a random color
            color = self.get_random_color()

            # if you cant have duplicate colors check if the color is already in the code
            if not self.Game.duplicate_color:
                # if the color is already in the code then just pick a new one until you get one that is not in the code
                while color in secret_code:
                    color = self.get_random_color()

            # add the random color to the code
            secret_code.append(color)

        # save the code in the game and return it.
        Game.code = secret_code
        return secret_code

    def get_random_color(self):
        return Color(random.randint(0, self.Game.number_of_colors - 1))

    def get_all_results(self):
        # get all placed pins from the database
        pins = Pin.query.filter_by(game_id=self.Game.id).all()

        # sort the pins in a dictionary that has the y positions as keys and as values an array of pins
        # this makes it so every row is separated
        sorted_pins = self.sort_pins(pins)

        # array to save all the results
        all_results = []

        # go through all the keys aka rows and get the results
        for key in sorted_pins.keys():
            all_results.append(self.guess_the_code(sorted_pins[key]))

        return all_results

    def sort_pins(self, pins):
        sorted_pins = {}
        for pin in pins:
            # get all the keys and store them in a list
            key_list = sorted_pins.keys()

            # check if the y coordinate is already in the key list
            if pin.y in key_list:

                # if so then get the already existing array add this pin and save it back in the dictionary
                pin_array = sorted_pins[pin.y]
                pin_array.append(pin)
                sorted_pins[pin.y] = pin_array

            else:
                # if not then make a new array that contains this pin and add this to the dictionary
                sorted_pins[pin.y] = [pin]

        return sorted_pins

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
