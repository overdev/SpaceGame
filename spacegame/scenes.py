__author__ = 'Jorge A. Gomes'


from ui import Dispatcher
from ui import Button
from geometry import *
from core import Scene
from core import Display
#from .core import resource
import pygame
import pygame.locals as c


__all__ = [

]


class SceneMain(Scene):

    class NewGameButton(Button):

        def on_left_click(self, client):
            """Stars a new game."""
            Scene.goto(None)

        def on_command(self):
            """Ends the game."""
            Scene.goto(None)

    class EndGameButton(Button):

        def on_left_click(self, client):
            """Exits the game."""
            Scene.goto(None)

    @classmethod
    def play(cls):

        dispatcher = Dispatcher(
            [cls.NewGameButton(Vec(100, 100), Vec(100, 20), "New Game", None),
            cls.EndGameButton(Vec(100, 150), Vec(100, 20), "End Game", None)]
        )
        dispatcher.listeners[0].command = (c.K_ESCAPE)
        clock = pygame.time.Clock()

        while Scene.get_current() is cls:
            clock.tick(30)
            events = pygame.event.get()
            dispatcher.process_events(events)

            Display.clear()

            surface = Display.surface()
            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen()