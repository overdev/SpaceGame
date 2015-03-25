"""SpaceGame

A simple 2d space shooter made with python and pygame.
"""

# Make sure you have python34 and pygame 1.9.1+ installed before run this code.
import pygame
from spacegame import scenes
from spacegame import core

if __name__ == "__main__":
    pygame.init()
    core.Game.run(scenes.SceneMain)