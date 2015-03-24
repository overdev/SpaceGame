__author__ = "Jorge A. Gomes"

import os
from os import path
import pygame

__all__ = [
    "Game",
    "Scene",
    "resource",
    "Vec"
]


def resource(name) -> str:
    """Returns the full path of a file with given name."""
    cwd = os.getcwd()
    rd = '{}\\res\\{}'.format(cwd, name)
    return rd


class Game(object):

    """The game launcher."""

    @classmethod
    def run(cls, scene) -> None:
        """Starts the game by running the first scene."""

        Display.show((800, 600))

        cls.scene = scene

        # while there's a scene set
        while cls.scene is not None:
            # plays this scene
            cls.scene.play()


class Display(object):

    @classmethod
    def show(cls, size, flags=0) -> None:
        pygame.display.set_mode(size, flags)

    @classmethod
    def surface(cls) -> pygame.Surface:
        return pygame.display.get_surface()

    @classmethod
    def size(cls) -> tuple:
        return cls.surface().get_size()

    @classmethod
    def clear(cls, color=(0, 0, 0)) -> None:
        cls.surface().fill(color)

    @classmethod
    def on_screen(cls) -> None:
        pygame.display.flip()


class Scene(object):

    """Base class for all game scenes.

    A scene is a piece of logic that guides the game flow. It can be a game level, a options menu screen
    or anything else similar. Every Scene has a particular way of handling input events and render
    stuff on the screen."""

    @classmethod
    def goto(cls, scene) -> None:
        """Sets the next scene to be played."""
        Game.scene = scene

    @classmethod
    def get_current(cls) -> object:
        """Returns the current Game scene being played."""
        return Game.scene

    @classmethod
    def play(cls) -> None:
        """Runs the game under this specific logic.

        Important: release all resources used in this scene when it finishes playing
        (when this method returns).

        Must be overridden by subclasses."""
        pass