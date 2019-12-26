from enum import Enum

class data(Enum):
    command = 1
    text = 2
    file = 3
    video = 4


class worker_type(Enum):
    listener = 1
    sender = 2
    toserver = 3
    gui = 4

class command_type(Enum):
    login = 1
    establish = 2
    disconnect = 3
    logout = 4
    query=5
    hi = 6
    reject = 7

