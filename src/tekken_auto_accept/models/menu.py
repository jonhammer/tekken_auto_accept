import time
from typing import List


class TekkenMenu(object):
    def __init__(self, state_name: str, commands: List[str], sleep: int = 0):
        self.state_name = state_name
        self.commands = commands
        self.sleep = sleep

    def run(self) -> List[str]:
        if self.sleep:
            time.sleep(self.sleep)

        return self.commands
