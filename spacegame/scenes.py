__author__ = 'Jorge A. Gomes'


from spacegame.ui import Dispatcher
from spacegame.ui import Button
from spacegame.ui import BitmapFont
from spacegame.geometry import *
from spacegame.core import Scene
from spacegame.core import Display
from spacegame.assets import *
from spacegame.actors import *
from spacegame.vectors import Vector
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
            dispatcher.process_events(events, game)

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
            dispatcher.process_events(events, game)

            Display.clear(fillcolor)
            surface = Display.surface()

            BitmapFont.render(surface, "Options", BitmapFont.large, (0, 0))
            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen(30)


class SceneGame(Scene):

    class Square(Actor):

        points = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]

        def __init__(self, position: Vector, rotation: float, scale: Vector):
            super(SceneGame.Square, self).__init__(SceneGame.Square.points)
            self.position = position
            self.rotation = rotation
            self.scale = scale

        def on_animation_end(self, attr: str, pathstate: PathState, game: type) -> None:
            """Back to previous scene."""
            game.scene = SceneMain


    @classmethod
    def play(cls, game: type) -> None:

        dispatcher = Dispatcher(
            [
                SceneOption.BackButton(Vec(100, 100), Vec(100, 40), "Back", None)
            ]
        )

        sq = cls.Square(Vector(50, 50), 0, Vector(20, 30))
        # sq.set_path('rotation', Path1d([0, 180, 10, 30, 0], True), AssignMode.direct_value, -1)
        sq.set_path(
            'scale',
            Path2d(
                [
                    (0, 0), (50, 10), (10, 50), (100, 100), (0, 0)
                ],
                False
            ),
            AssignMode.vector_updt,
            -1)
        # sq.paths['rotation'].set_animation(repeats=1)
        room = Room(
            [
                sq
            ]
        )
        textcolor = (0, 0, 92)
        fillcolor = (0, 0, 16)
        BitmapFont.set_colors(BitmapFont.large, fillcolor, textcolor)

        while game.scene is cls:
            events = pygame.event.get()
            dispatcher.process_events(events, game)
            room.update(room.view, game)

            Display.clear(fillcolor)
            surface = Display.surface()

            BitmapFont.render(surface, "Game", BitmapFont.large, (0, 0))

            for actor in room.actors:
                actor.default_render(surface, room.view)

            for gui in dispatcher.listeners:
                gui.basic_render(surface)

            Display.on_screen(60)
