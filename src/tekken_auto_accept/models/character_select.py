import logging
import os

from tekken_auto_accept.errors import CharacterNotFound
from tekken_auto_accept.models.screen_state import ScreenState
from tekken_auto_accept.settings import CHARACTERS

logger = logging.getLogger(__name__)


class CharacterSelect(object):
    def __init__(self):
        self.desired_char = None
        self.selected_char = None

        self.current_row = None
        self.current_col = None
        self.desired_row = None
        self.desired_col = None

        self.moves = []

        self.portraits = None
        self.scanner = ScreenState()

    def get_portraits(self, side):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.abspath(os.path.join(dir_path, "..", "data", "chars"))
        if side == "p1":
            self.portraits = [i for i in os.listdir(data_path) if "p2" not in i]
        else:
            self.portraits = [i for i in os.listdir(data_path) if "p2" in i]
        self.portraits = [os.path.join(data_path, i) for i in self.portraits]

    def run(self):
        self.desired_row, self.desired_col = self.get_char_location(self.desired_char)
        logger.debug(f"Desired: {self.desired_row}, {self.desired_col}")
        self.get_currently_selected()
        self.current_row, self.current_col = self.get_char_location(self.selected_char)
        logger.debug(f"Current: {self.current_row}, {self.current_col}")
        self.get_moves()
        logger.debug(f"Moves: {self.moves}")
        return self.moves

    def get_currently_selected(self):

        for _i in range(3):
            character = self.scanner.scan_screen(self.portraits)
            if character:
                self.selected_char = character.replace(".png", "").replace("-p2", "")
                logger.debug(f"Got char {character}")
                return
        raise CharacterNotFound("Could not find any character")

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
            self.current_col += 2
        elif self.current_row == 2 and self.current_col in [0, 1, 2]:
            self.current_row = 1
            return
        elif self.current_row == 2 and self.current_col in [16, 17, 18]:
            self.current_row = 1
            return
        self.current_row = self.current_row + 1

    def move_up(self):
        self.moves.append("up")
        if self.current_row == 1 and self.current_col in [0, 1, 2]:
            self.current_row = 0
            self.current_col = 0
            return
        if self.current_row == 1 and self.current_col in [16, 17, 18]:
            self.current_row = 0
            self.current_col = 13
            return

        if self.current_row == 0:
            self.current_col += 2
        if self.current_row == 1:
            self.current_col -= 2

        self.current_row = self.current_row - 1

    def move_right(self):
        self.moves.append("right")
        self.current_col = (self.current_col + 1) % len(CHARACTERS[self.current_row])

    def move_left(self):
        self.moves.append("left")
        self.current_col = (self.current_col - 1) % len(CHARACTERS[self.current_row])

    def get_moves(self):
        while True:
            if len(self.moves) > 50:
                raise IndexError
            if self.current_row > self.desired_row:
                self.move_up()
                continue
            if self.current_row < self.desired_row:
                self.move_down()
                continue
            if self.current_col < self.desired_col:
                self.move_right()
                continue
            if self.current_col > self.desired_col:
                self.move_left()
                continue
            if (
                self.current_row == self.desired_row
                and self.current_col == self.desired_col
            ):
                break
        self.moves.append("b")

    def no_select(self):
        return None
