import os

import pyautogui


class ScreenState(object):
    def __int__(self):
        self.current_screen = None

    def scan_screen(self, images: str) -> str:
        """
        Scan the screen for the list of images
        :param images: List of image file paths
        :return: Name of image found
        """
        for image in images:
            self.current_screen = pyautogui.screenshot()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_path = os.path.abspath(os.path.join(dir_path, '..', 'data'))
            if pyautogui.locate(
                    os.path.join(data_path, image),
                    self.current_screen,
                    confidence=0.9,
            ):
                print("Found {}".format(image))
                return image
