from .Types     import UserInput
from .Factories import APIFactory


class API():
    def __init__(self):
        pass

    def NewUser(self):
        pass

    def AcceptInput(self, input: UserInput):
        pass


def Get():
    return APIFactory.Make()

