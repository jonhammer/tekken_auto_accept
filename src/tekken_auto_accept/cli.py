import argparse
import os
from abc import ABC, abstractmethod
from typing import List
from time import sleep

import pyautogui

SIDE_MAP = {"left": ["enter"], "right": ["left", "enter"]}

CHARACTER_MAP = {"test": ["left, left", "left", "enter"]}


def create_parser():
    """Parses command line args."""
    epilog = """

        e.g., tekken_auto_accept -c marduk

    """
    parser = argparse.ArgumentParser(
        description="Auto accept ranked matches", epilog=epilog,
    )
    parser.add_argument(
        "-c", "--character",
    )
    parser.add_argument(
        "-s", "--side",
    )
    parser.add_argument(
        "-r",
        "--rematch",
        help="Auto re-match after 5 seconds",
        default=False,
        action="store_true",
    )
    return parser


class MenuState(ABC):
    def __init__(self, state_name: str, image: str, commands: List[str]):
        self.state_name = state_name
        self.image = image
        self.commands = commands

    def run(self) -> bool:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        coordinates = self.find_image(os.path.join(dir_path, 'data', self.image))
        if coordinates:
            if self.state_name == 'post_match':
                sleep(5)
            for command in self.commands:
                pyautogui.press(command)
            return True

    @staticmethod
    def find_image(image) -> List[int]:
        coordinates = pyautogui.locateOnScreen(image)
        if coordinates:
            return coordinates


class TekkenState:

    states_data = {
        "main_menu": {"image": "main_menu.PNG", "commands": ["down", "enter"],},
        "online_menu": {"image": "online_menu.PNG", "commands": ["enter"],},
        "ranked_search_menu": {
            "image": "ranked_search_menu.PNG",
            "commands": ["up", "enter"],
        },
        "side_select": {"image": "side_select.PNG", "commands": ["enter"],},
        "character_select": {"image": "character_select.PNG", "commands": "enter",},
        "new_challenger": {"image": "new_challenger.PNG", "commands": ["enter"],},
        "post_match": {"image": "post_match.PNG", "commands": ["enter"],},
        "no_rematch": {"image": "no_rematch.PNG", "commands": ["enter"]},
    }

    def __init__(self):
        self.current_state_name = None
        self.startup = True

        self.current_state = None

        self.main_menu = None
        self.online_menu = None
        self.ranked_search_menu = None
        self.side_select = None
        self.character_select = None
        self.ranked_lobby = None
        self.post_match = None

        for state, state_data in self.states_data.items():
            image = state_data["image"]
            commands = state_data["commands"]

            setattr(self, state, MenuState(state, image, commands))

    def scan_state(self):
        for state_name, state_data in self.states_data.items():
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if pyautogui.locateOnScreen(os.path.join(dir_path, 'data', state_data["image"])):
                if self.startup:
                    self.startup = False
                self.set_state(state_name)
                return True

    def set_state(self, state_name):
        self.current_state_name = state_name
        self.current_state = getattr(self, state_name)

    def get_state(self, state_name):
        return getattr(self, state_name)

    def run(self):
        while True:
            self.scan_state()
            if not self.startup and self.current_state_name in [
                "ranked_lobby",
                "post_match",
            ]:
                self.current_state = self.get_state(self.current_state_name)
                self.current_state.run()
            else:
                self.current_state.run()


def main():
    parser = create_parser()
    args = parser.parse_args()
    tekken_state = TekkenState()
    if args.side:
        tekken_state.states_data["side_select"]["commands"] = SIDE_MAP["args.side"]
    if args.character:
        tekken_state.states_data["character_select"]["commands"] = CHARACTER_MAP[
            "args.character"
        ]

    tekken_state.current_state_name = "main_menu"
    tekken_state.run()


if __name__ == '__main__':
    main()