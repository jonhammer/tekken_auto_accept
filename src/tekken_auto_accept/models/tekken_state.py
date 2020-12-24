import os
import logging
from random import randint

from tekken_auto_accept.models.character_select import CharacterSelect
from tekken_auto_accept.models.menu import TekkenMenu
from tekken_auto_accept.settings import MENU_DATA


logger = logging.getLogger(__name__)


class TekkenState:
    def __init__(self):
        self.selected_char = False

        self.current_state_name = "main_menu"
        self.previous_state_name = None
        self.current_state = None
        self.current_screen = None
        self.alert = None
        self.rematch = None

        self.in_startup = True

        self.main_menu = None
        self.online_menu = None
        self.ranked_search_menu = None
        self.side_select = None
        self.character_select = None
        self.ranked_lobby = None
        self.post_match = None

        for state, state_data in MENU_DATA.items():
            commands = state_data["commands"]
            if state == 'character_select':
                setattr(self, state, CharacterSelect())
            else:
                setattr(self, state, TekkenMenu(state, commands))

        self.set_state(self.current_state_name)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.abspath(os.path.join(dir_path, '..', 'data'))
        self.state_images = [os.path.join(data_path, i) for i in os.listdir(data_path) if '.png' in i.lower()]
        loading_image = next((i for i in self.state_images if 'loading' in i), None)
        new_challenger_image = next((i for i in self.state_images if 'new_challenger' in i), None)
        post_match_image = next((i for i in self.state_images if 'post_match' in i), None)
        for i in range(len(self.state_images) // 3):
            self.state_images.insert(randint(0, len(self.state_images) - 1), new_challenger_image)
            self.state_images.insert(randint(0, len(self.state_images) - 1), loading_image)
            self.state_images.insert(randint(0, len(self.state_images) - 1), post_match_image)

    def process_config(self, tekken_config):
        self.character_select.desired_char = tekken_config.character
        self.character_select.get_portraits(tekken_config.side)
        if tekken_config.side == 'p2':
            self.side_select.commands = ["right", "b"]
        self.alert = tekken_config.alert
        self.rematch = tekken_config.rematch

    def set_state(self, state_name):
        logger.debug("Setting state to {}".format(state_name))
        self.current_state_name = state_name
        self.current_state = getattr(self, state_name)

    def get_state(self, state_name):
        return getattr(self, state_name)
