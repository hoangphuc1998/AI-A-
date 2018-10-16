from enum import Enum


class Type(Enum):
    Empty = 0
    Obstacle = 1
    Opened = 2
    Closed = 3
    Start = 4
    Goal = 5
    Path = 6


class Croodinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setCrood(self, x, y):
        self.x = x
        self.y = y

    def getCrood(self):
        return self.x, self.y
