__author__ = 'Conor'

# Enums -> http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
# Coding Standards -> https://www.python.org/dev/peps/pep-0008/

from enum import Enum


class Config(Enum):
    """
    Class to store enumerations for the configuration file for readability
    """
    PUB_ADDR = 0
    SUB_ADDR = 1
    TOPIC = 2
    FIREBASE_URL = 3
    HEARTBEAT_ADDR = 4
    HEARTBEAT_TOPIC = 5
    RESPONSE_TOPIC = 6
    SERVICE_NAME = 7
