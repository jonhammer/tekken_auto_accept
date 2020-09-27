import os
import time

import pyautogui

from control import TekkenController
from models.menu import MenuState


class TekkenState:

    states_data = {
        "main_menu": {
            "image": "main_menu.PNG",
            "commands": ["down", "b"],
        },
        "online_menu": {
            "image": "online_menu.PNG",
            "commands": ["b"],
        },
        "ranked_search_menu": {
            "image": "ranked_search_menu.PNG",
            "commands": ["up", "b"],
        },
        "side_select": {
            "image": "side_select.PNG",
            "commands": ["b"],
        },
        "character_select": {
            "image": "character_select.PNG",
            "commands": "b",
        },
        "new_challenger": {
            "image": "new_challenger.PNG",
            "commands": ["b"],
        },
        "post_match": {
            "image": "post_match.PNG",
            "commands": ["b"],
        },
        "no_rematch": {"image": "no_rematch.PNG", "commands": ["b"]},
    }

    def __init__(self, character, side):
        self.controller = TekkenController()
        self.character = character
        self.side = side
        self.selected_char = False

        if self.side == 'p2':
            self.states_data['side_select']['commands'] = ["right", "b"]

        self.current_state_name = "main_menu"
        self.current_state = None
        self.current_screen = None

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

            setattr(self, state, MenuState(state, image, commands, self))

        self.set_state(self.current_state_name)

    def scan_state(self):
        if self.selected_char:
            time.sleep(1)
        for state_name, state_data in self.states_data.items():
            self.current_screen = pyautogui.screenshot()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_path = os.path.abspath(os.path.join(dir_path, '..', 'data'))
            if pyautogui.locate(
                os.path.join(data_path, state_data["image"]),
                self.current_screen,
                confidence=0.9,
            ):
                print("Found {}".format(state_data["image"]))
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
            if self.selected_char:
                time.sleep(1)
            if self.scan_state():
                commands = self.current_state.run()
                self.controller.run_commands(commands)
