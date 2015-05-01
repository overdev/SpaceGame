__author__ = 'Jorge A. Gomes'


from spacegame.ui import Dispatcher
from spacegame.ui import Button
from spacegame.ui import BitmapFont
from spacegame.ui import Anchor
from spacegame.geometry import *
from spacegame.core import Scene
from spacegame.core import Display
from spacegame.core import resource
from spacegame.assets import *
from spacegame.actors import *
from spacegame.vectors import Vector
import random
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
            game.goto(SceneGame)

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

        textcolor = (128, 0, 0)
        fillcolor = (32, 0, 0)
        BitmapFont.set_colors(BitmapFont.large, fillcolor, textcolor)

        while game.scene is cls:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            dispatcher.process_events(events, keys, game)

            Display.clear(fillcolor)
            surface = Display.surface()

            BitmapFont.render(surface, "Main", BitmapFont.large, (0, 0), c.BLEND_RGB_ADD)

            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen(30)


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
    def play(cls, game: type) -> None:

        dispatcher = Dispatcher(
            [
                cls.BackButton(Vec(100, 100), Vec(100, 40), "Back", None)
            ]
        )
        # dispatcher.listeners[0].command = (c.K_ESCAPE)
        textcolor = (0, 128, 128)
        fillcolor = (0, 32, 32)
        BitmapFont.set_colors(BitmapFont.large, fillcolor, textcolor)

        while game.scene is cls:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            dispatcher.process_events(events, keys, game)

            Display.clear(fillcolor)
            surface = Display.surface()

            BitmapFont.render(surface, "Options", BitmapFont.large, (0, 0))
            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen(30)


class SceneGame(Scene):

    class Starship(Actor):

        refpoints = [(0.5, 0.0), (0.4, 0.2), (-0.3, 0.5), (-0.3, 0.3), (-0.5, 0.0),
            (-0.3, -0.3), (-0.3, -0.5), (0.4, -0.2)]

        def __init__(self, position: Vector, rotation: float, scale: Vector):
            super(SceneGame.Starship, self).__init__(SceneGame.Starship.refpoints)
            self.position.xy = position
            self.rotation = rotation
            self.scale.xy = scale
            self.fillcolor = (0, 0, 255)
            self.linecolor = (64, 64, 255)

        def on_keydown(self, keys: tuple, game: type, room: Room) -> None:
            if keys[c.K_w]:
                self.motion_add(0.1, self.rotation)
            if keys[c.K_a]:
                self.rotation = (self.rotation + 4) % 360
            if keys[c.K_d]:
                self.rotation = (self.rotation - 4) % 360

            room.view.motion = self.motion

        def on_prerender(self, game: type, room: 'Room') -> None:
            room.view.follow(self.position)

    @classmethod
    def play(cls, game: type) -> None:

        dispatcher = Dispatcher(
            [
                SceneOption.BackButton(Vec(100, 540), Vec(100, 40), "Back", None)
            ]
        )
        room = Room([
            cls.Starship(Vector(300, 200), 0, Vector(50, 50))
        ])

        textcolor = (0, 0, 92)
        fillcolor = (0, 0, 16)
        BitmapFont.set_colors(BitmapFont.large, fillcolor, textcolor)

        while game.scene is cls:
            Display.clear(fillcolor)
            surface = Display.surface()

            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            dispatcher.process_events(events, keys, game)
            room.update(events, keys, room.view, game)

            BitmapFont.render(surface, "Game", BitmapFont.large, (0, 0))

            room.view.render(surface)
            for actor in room.actors:
                actor.default_render(surface, room.view)

            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen(60)
