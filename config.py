__author__ = 'Conor'

# Enums -> http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python

from enum import Enum


class Config(Enum):
    PUB_ADDRESS = 0
    SUB_ADDRESS = 1
    TOPIC = 2
    FIREBASE_URL = 3
