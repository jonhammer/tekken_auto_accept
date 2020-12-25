import os
import sys

from tekken_auto_accept.settings import MENU_ORDER


def probable_next_state(state):
    current_index = MENU_ORDER.index(next((i for i in MENU_ORDER if state in i), None))
    try:
        return MENU_ORDER[current_index + 1]
    except IndexError:
        return MENU_ORDER[0]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)