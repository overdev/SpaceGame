__author__ = 'Jorge A. Gomes'


from .ui import Dispatcher
from .geometry import *
from .core import Scene
from .core import resource
import pygame
import pygame.locals as c


__all__ = [

]


class SceneMain(Scene):

    @classmethod
    def play(cls):
        pass