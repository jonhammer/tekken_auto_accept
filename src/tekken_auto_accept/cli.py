import argparse
import os
from abc import ABC, abstractmethod
from typing import List
from time import sleep

import pyautogui

from tekken_auto_accept.control import TekkenController

SIDE_MAP = {"left": ["b"], "right": ["left", "b"]}

CHARACTER_MAP = {"test": ["left, left", "left", "b"]}


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

    def run(self) -> List[str]:
        if self.state_name == "post_match":
            sleep(3)
        return self.commands

    @staticmethod
    def find_image(image) -> List[int]:
        coordinates = pyautogui.locateOnScreen(image, confidence=0.9)
        if coordinates:
            return coordinates


class TekkenState:

    states_data = {
        "main_menu": {"image": "main_menu.PNG", "commands": ["down", "b"],},
        "online_menu": {"image": "online_menu.PNG", "commands": ["b"],},
        "ranked_search_menu": {
            "image": "ranked_search_menu.PNG",
            "commands": ["up", "b"],
        },
        "side_select": {"image": "side_select.PNG", "commands": ["b"],},
        "character_select": {"image": "character_select.PNG", "commands": "b",},
        "new_challenger": {"image": "new_challenger.PNG", "commands": ["b"],},
        "post_match": {"image": "post_match.PNG", "commands": ["b"],},
        "no_rematch": {"image": "no_rematch.PNG", "commands": ["b"]},
    }

    def __init__(self):
        self.controller = TekkenController()

        self.current_state_name = "main_menu"
        self.current_state = None

        self.in_startup = True

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

        self.set_state(self.current_state_name)

    def scan_state(self):
        if not self.in_startup:
            sleep(1)
        for state_name, state_data in self.states_data.items():
            current_screen = pyautogui.screenshot()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if pyautogui.locate(
                os.path.join(dir_path, "data", state_data["image"]), current_screen, confidence=0.9
            ):
                print("Found {}".format(state_data['image']))
                self.set_state(state_name)
                return True

    def set_state(self, state_name):
        print("Setting state to {}".format(state_name))
        self.current_state_name = state_name
        self.current_state = getattr(self, state_name)

    def get_state(self, state_name):
        return getattr(self, state_name)

    def run(self):
        while True:
            if self.scan_state():
                commands = self.current_state.run()
                if self.current_state_name == 'character_select':
                    self.in_startup = False

                if not self.in_startup and self.current_state_name in ['new_challenger', 'post_match', 'no_rematch']:
                    self.controller.run_commands(commands)
                elif self.in_startup:
                    self.controller.run_commands(commands)


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

    tekken_state.run()


if __name__ == "__main__":
    main()
