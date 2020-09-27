import os
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