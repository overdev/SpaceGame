__author__ = 'Jorge'


import pygame
from spacegame.geometry import *
from spacegame.vectors import Vector


__all__ = [

]


class Actor(object):

    """Base class for all in-game objects."""

    def __init__(self):
        self.position = Vector.zero()
        self.motion = Vector.zero()
        self.heading = 0

    def motion_update(self) -> None:
        """Updates position by adding motion to it."""
        self.position += self.motion
