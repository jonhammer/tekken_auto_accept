# Taken from:
# https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game

import ctypes
import logging
from time import sleep


logger = logging.getLogger(__name__)


SendInput = ctypes.windll.user32.SendInput


PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


class P2_MAP:
    UP = 0xC8
    DOWN = 0xD0
    LEFT = 0xCB
    RIGHT = 0xCD
    A = 0x4B
    B = 0x4C
    X = 0x47
    Y = 0x48
    START = 0xC7
    SELECT = 0xD2
    LB = 0x49
    RB = 0x4D
    LT = 0x4A
    RT = 0x4E


"""
class P1_MAP:
    UP = 0x11
    DOWN = 0x1F
    LEFT = 0x1E
    RIGHT = 0x20
    A = 0x24
    B = 0x25
    X = 0x16
    Y = 0x17
    START = 0x30
    SELECT = 0x2F
    LB = 0x19
    RB = 0x18
    LT = 0x27
    RT = 0x26
"""


class P1_MAP:
    UP = 0xC8
    DOWN = 0xD0
    LEFT = 0xCB
    RIGHT = 0xCD
    A = 0x24
    B = 0x25
    X = 0x16
    Y = 0x17
    START = 0x30
    SELECT = 0x2F
    LB = 0x19
    RB = 0x18
    LT = 0x27
    RT = 0x26


def press_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def tap_key(hex_key_code):
    press_key(hex_key_code)
    sleep(0.1)
    release_key(hex_key_code)
    sleep(0.2)


class TekkenController:
    def __init__(self, is_p1=True):
        self.is_p1 = is_p1
        if self.is_p1:
            self.map = P1_MAP
        else:
            self.map = P2_MAP

    def do_input(self, input_string):
        logger.debug(f"Pressing {input_string}")
        input_method = getattr(self, input_string)
        input_method()

    def up(self):
        tap_key(self.map.UP)

    def down(self):
        tap_key(self.map.DOWN)

    def left(self):
        tap_key(self.map.LEFT)

    def right(self):
        tap_key(self.map.RIGHT)

    def a(self):
        tap_key(self.map.A)

    def b(self):
        tap_key(self.map.B)

    def forward(self):
        self.b()

    def x(self):
        tap_key(self.map.X)

    def y(self):
        tap_key(self.map.Y)

    def start(self):
        tap_key(self.map.START)

    def select(self):
        tap_key(self.map.SELECT)

    def run_commands(self, commands):
        for command in commands:
            self.do_input(command)
