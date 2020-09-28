from tekken_auto_accept.settings import MENU_ORDER


def probable_next_state(state):
    current_index = MENU_ORDER.index(next((i for i in MENU_ORDER if state in i), None))
    try:
        return MENU_ORDER[current_index + 1]
    except IndexError:
        return MENU_ORDER[0]