import http.client
import os
import urllib
from abc import ABC, abstractmethod

from playsound import playsound


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
    def trigger(self):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode(
                {
                    "token": "TOKEN",
                    "user": "USER",
                    "message": "Found Tekken match",
                }
            ),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()
