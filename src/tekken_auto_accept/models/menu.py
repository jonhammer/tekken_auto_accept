import time
from typing import List

from tekken_auto_accept.alerts import PushOver
from tekken_auto_accept.models.character_select import CharacterSelect


class MenuState(object):
    def __init__(self, state_name: str, image: str, commands: List[str], tekken_state):
        self.state_name = state_name
        self.image = image
        self.commands = commands
        self.tekken_state = tekken_state

    def run(self) -> List[str]:
        if self.state_name == "post_match":
            time.sleep(1)
        elif self.state_name == 'character_select':
            select_screen = CharacterSelect(self.tekken_state.character, self.tekken_state.side)
            select_screen.get_moves()
            print("Got moves: {}".format(select_screen.moves))
            self.commands = select_screen.moves
            self.tekken_state.selected_char = True
        elif self.state_name == 'loading':
            alert = PushOver()
            alert.trigger()

        return self.commands
