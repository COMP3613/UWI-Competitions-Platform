from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, reciever=None):
        self.reciever = reciever

    @abstractmethod
    def execute(self):
        pass
