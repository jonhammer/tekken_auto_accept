import os

import pyautogui

CHARACTERS = [
    [
        "ganryu",
        "zafina",
        "julia",
        "marduk",
        "anna",
        "geese",
        "eliza",
        "noctis",
        "lei",
        "aking",
        "negan",
        "leroy",
        "fahk",
    ],
    [
        "raven",
        "nina",
        "yoshimitsu",
        "dragunov",
        "hwoarang",
        "law",
        "shaheen",
        "akuma",
        "kazuya",
        "random",
        "heihachi",
        "kazumi",
        "chloe",
        "lili",
        "lars",
        "ling",
        "jack",
        "lee",
        "kuma",
    ],
    [
        "miguel",
        "bob",
        "bryan",
        "king",
        "steve",
        "paul",
        "josie",
        "katarina",
        "jin",
        "random",
        "dvj",
        "claudio",
        "gigas",
        "asuka",
        "alisa",
        "leo",
        "feng",
        "eddy",
        "kuma",
    ],
]


class CharacterSelect(object):
    def __init__(self, desired_char, side):
        self.side = side
        self.desired_char = desired_char
        self.selected_char = None

        self.get_currently_selected()
        print(self.selected_char)
        print(self.desired_char)

        self.current_row, self.current_col = self.get_char_location(self.selected_char)
        self.desired_row, self.desired_col = self.get_char_location(self.desired_char)
        print(self.desired_row, self.desired_col)

        self.moves = []

    def get_currently_selected(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.abspath(os.path.join(dir_path, '..', 'data', 'chars'))
        if self.side == 'p1':
            portraits = [i for i in os.listdir(data_path) if 'p2' not in i]
        else:
            portraits = [i for i in os.listdir(data_path) if 'p2' in i]
        portraits = os.listdir(data_path)
        print(portraits)
        current_screen = pyautogui.screenshot()
        for _i in range(3):
            print("looking for char on {}".format(self.side))
            for portrait in portraits:
                if pyautogui.locate(
                        os.path.join(data_path, portrait),
                        current_screen,
                        confidence=0.9,
                        grayscale=True
                ):
                    self.selected_char = portrait.replace('.png', '').replace('-p2', '')
                    print("Got char {}".format(portrait))
                    return

    @staticmethod
    def get_char_location(character):
        char_row = None
        char_col = None
        for i, row in enumerate(CHARACTERS):
            if character in row:
                char_row = i
            for i2, col in enumerate(row):
                if col == character:
                    char_col = i2
        return char_row, char_col

    def move_down(self):
        self.moves.append("down")
        if self.current_row == 0:
            self.current_col += 3
        elif self.current_row == 2 and self.current_col in [0, 1, 2]:
            self.current_row = 1
            return
        elif self.current_row == 2 and self.current_col in [16, 17, 18]:
            self.current_row = 1
            return
        self.current_row = (self.current_row + 1) % 3

    def move_up(self):
        self.moves.append("up")
        if self.current_row == 0:
            self.current_col += 3
        elif self.current_row == 1 and self.current_col in [0, 1, 2]:
            self.current_row = 0
            self.current_col = 0
            return
        elif self.current_row == 1 and self.current_col in [16, 17, 18]:
            self.current_row = 0
            self.current_col = 11
            return
        elif self.current_row == 1:
            self.current_col -= 3
        self.current_row = (self.current_row - 1) % 3

    def move_right(self):
        self.moves.append("right")
        self.current_col = (self.current_col + 1) % len(CHARACTERS[self.current_row])

    def move_left(self):
        self.moves.append("left")
        self.current_col = (self.current_col - 1) % len(CHARACTERS[self.current_row])

    def get_moves(self):
        while True:
            if self.current_row != self.desired_row:
                self.move_up()
                continue
            if self.current_col < self.desired_col:
                self.move_right()
                continue
            elif self.current_col > self.desired_col:
                self.move_left()
                continue
            self.moves.append('b')
            break
