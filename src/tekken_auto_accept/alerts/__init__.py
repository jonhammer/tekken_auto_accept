import requests
import os
from abc import ABC, abstractmethod

from playsound import playsound

from tekken_auto_accept.errors import AlertError


class Alert(ABC):
    @abstractmethod
    def trigger(self):
        pass


class Sound(Alert):
    def trigger(self):
        data_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", "data", "alerts"
        )
        data_path = os.path.abspath(data_path)
        playsound(os.path.join(data_path, "alert.mp3"))


class PushOver(Alert):

    URL = "https://api.pushover.net/1/messages.json"

    def __int__(self):
        self.app_token = None
        self.user_token = None

    def trigger(self):
        data = {
            "token": self.app_token,
            "user": self.user_token,
            "message": "Found Tekken Match",
            "priority": 1,
        }
        response = requests.post(self.URL, data=data)
        if not response.status_code == 200:
            raise AlertError("Unable to send PushOver Alert")
