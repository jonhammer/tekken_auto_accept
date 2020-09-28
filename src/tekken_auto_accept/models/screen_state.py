import os
from typing import List

import pyautogui


class ScreenState(object):
    def __init__(self):
        self.current_screen = None

    def capture_screen(self):
        self.current_screen = pyautogui.screenshot()

    def scan_screen(self, images: List[str]) -> str:
        """
        Scan the screen for the list of images
        :param images: List of image file paths
        :return: Name of image found
        """
        self.capture_screen()
        for image in images:
            #print("looking for {}".format(image))
            image_name = os.path.basename(image).lower().replace('.png', '')
            if pyautogui.locate(
                    image,
                    self.current_screen,
                    confidence=0.9,
            ):
                print("Found {}".format(image_name))
                return image_name
