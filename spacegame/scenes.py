__author__ = 'Jorge A. Gomes'


from spacegame.ui import Dispatcher
from spacegame.ui import Button
from spacegame.ui import BitmapFont
from spacegame.geometry import *
from spacegame.core import Scene
from spacegame.core import Display
import pygame
import pygame.locals as c


__all__ = [
    "SceneMain"
]


class SceneMain(Scene):

    class NewGameButton(Button):

        def on_initialize(self) -> None:
            self.command = (c.K_ESCAPE,)

        def on_left_click(self, client, game) -> None:
            """Go to Options scene."""
            game.goto(SceneOption)

        def on_command(self, game) -> None:
            """Go to Options scene."""
            game.goto(SceneOption)

    class EndGameButton(Button):

        def on_left_click(self, client, game) -> None:
            """Exits the game."""
            game.end()

    @classmethod
    def play(cls, game) -> None:
        dispatcher = Dispatcher(
            [
                cls.NewGameButton(Vec(100, 100), Vec(150, 40), "New Game", None),
                cls.EndGameButton(Vec(100, 150), Vec(150, 40), "End Game", None)
            ]
        )

        clock = pygame.time.Clock()
        textcolor = (128, 0, 0)
        fillcolor = (32, 0, 0)
        BitmapFont.set_colors(BitmapFont.large, fillcolor, textcolor)

        while game.scene is cls:
            clock.tick(30)
            events = pygame.event.get()
            dispatcher.process_events(events, game)

            Display.clear(fillcolor)
            surface = Display.surface()

            BitmapFont.render(surface, "Main", BitmapFont.large, (0, 0), c.BLEND_RGB_ADD)

            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen()


class SceneOption(Scene):

    class BackButton(Button):
        """The Back button."""

        def on_initialize(self) -> None:
            self.command = (c.K_b,)

        def on_left_click(self, client, game) -> None:
            """Go back to SceneMain"""
            game.goto(SceneMain)

        def on_command(self, game) -> None:
            """Go back to SceneMain"""
            game.goto(SceneMain)

    @classmethod
    def play(cls, game) -> None:

        dispatcher = Dispatcher(
            [
                cls.BackButton(Vec(100, 100), Vec(100, 40), "Back", None)
            ]
        )
        # dispatcher.listeners[0].command = (c.K_ESCAPE)
        clock = pygame.time.Clock()
        textcolor = (0, 128, 128)
        fillcolor = (0, 32, 32)
        BitmapFont.set_colors(BitmapFont.large, fillcolor, textcolor)

        while game.scene is cls:
            clock.tick(30)
            events = pygame.event.get()
            dispatcher.process_events(events, game)

            Display.clear(fillcolor)
            surface = Display.surface()

            BitmapFont.render(surface, "Options", BitmapFont.large, (0, 0))
            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen()

