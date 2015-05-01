__author__ = 'Jorge'


import pygame
import pygame.locals as c
from spacegame.geometry import *
from spacegame.vectors import Vector
from spacegame.assets import *
from spacegame.ui import Anchor, BitmapFont
from spacegame.core import resource


__all__ = [
    "Actor",
    "Room",
    "View"
]


class Actor(Polygon):

    """Base class for all in-game objects."""

    # NOTE: do not set __slots__, it will cause problems with the update method.

    def __init__(self, refpoints):
        super(Actor, self).__init__(Vector.zero(), 0.0, Vector.one(), refpoints)
        self.motion = Vector.zero()
        self.command = None
        self.paths = {}

    def set_path(self, attribute: str, path: Path, asgnmode: AssignMode, repeats: int=-1, ratio: float=0.0) -> None:
        """Adds or removes a animation path for an attribute."""
        if path is None:
            try:
                del self.paths[attribute]
            except KeyError:
                pass
        elif isinstance(path, Path):
            pth = PathState(attribute, asgnmode, path)
            pth.counter = repeats
            pth.ratio = ratio
            self.paths[attribute] = pth
        else:
            raise TypeError("'path' argument is not a Path subclass.")

    def motion_update(self) -> None:
        """Default motion update for this object"""
        self.position += self.motion

    def motion_add(self, length: float, angle: float) -> None:
        """apply motion to this object."""
        self.motion += lengthdir(length, angle)

    def animate(self, game: type) -> None:
        """Updates animation attributes."""

        # check for animations
        for name in self.__dict__:
            if name in self.paths:
                pathstate = self.paths[name]
                if pathstate.is_animating:
                    ended = pathstate.animate()
                    if pathstate.asgnmode is AssignMode.direct_value:
                        setattr(self, name, pathstate.position)
                    elif pathstate.asgnmode is AssignMode.vector_updt:
                        getattr(self, name).xy = pathstate.position
                    if ended:
                        self.on_animation_end(name, pathstate, game)

            else:
                if name == 'position':
                    self.motion_update()

    def on_initialize(self) -> None:
        """Called in the instance creation."""
        pass

    def on_animation_end(self, attr: str, pathstate: PathState, game: type, room: 'Room'):
        """Called when the animation for the attribute reaches the last step."""

    def on_collision(self, other: 'Actor', info: dict, game: type, room: 'Room'):
        """Called when this object collides with other."""
        pass

    def on_keydown(self, keys: tuple, game: type, room: 'Room') -> None:
        """Called whenever a keyboard key is down."""
        pass

    def on_keyup(self, key: int, game: type, room: 'Room') -> None:
        """Called whenever a keyboard key is released."""
        pass

    def on_left_click(self, inroom: Vector, inview: Vector, game: type, room: 'Room') -> None:
        """Called when the left mouse button is pressed."""
        pass

    def on_right_click(self, inroom: Vector, inview: Vector, game: type, room: 'Room') -> None:
        """Called when the right mouse button is pressed."""
        pass

    def on_middle_click(self, inroom: Vector, inview: Vector, game: type, room: 'Room') -> None:
        """Called when the middle mouse button is pressed."""
        pass

    def on_mouse_move(self, inroom: Vector, inview: Vector, motion: Vector, game: type, room: 'Room') -> None:
        """Called when the mouse moves over this object."""
        pass

    def on_client_exit(self, game: type, room: 'Room') -> None:
        """Called when the mouse moves out this object."""
        pass

    def on_roll_up(self, inroom: Vector, inview: Vector, game: type, room: 'Room') -> None:
        """Called when the mouse wheel rolls up."""
        pass

    def on_roll_down(self, inroom: Vector, inview: Vector, game: type, room: 'Room') -> None:
        """Called when the mouse wheel rolls down."""
        pass

    def on_enter_view(self, view: 'View', game: type, room: 'Room') -> None:
        """Called when the object gets partially or totally inside the view area."""

    def on_leave_view(self, view: 'View', game: type, room: 'Room') -> None:
        """Called when the object get totally outside the view area."""

    def on_command(self, cmd: tuple, game: type, room: 'Room') -> None:
        """Called when the this object's keyboard command is entered."""
        pass

    def on_prerender(self, game: type, room: 'Room') -> None:
        """Called right before the frame rendering."""
        pass


class View(Polygon):

    refpoints = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    transition = Path1d([0.75 ** i for i in range(20)])
    starfield = pygame.image.load(resource("starfield.png"))

    def __init__(self, room: 'Room'):
        super(View, self).__init__(Vector.zero(), 0.0, Vector(*self.size), View.refpoints)
        self.motion = Vector.zero()
        self.room = room
        self.anchor = Anchor.top_left
        self.paths = {}
        self.set_path('transition', View.transition, AssignMode.direct_value, 0)
        self.parallaxes = [
            BackScroller(View.starfield, self.size, [77, 14]),
            BackScroller(View.starfield, self.size, [28, 56]),
        ]

    @property
    def size(self) -> tuple:
        return pygame.display.get_surface().get_size()

    def rel_point(self, point: tuple) -> Vector:
        x, y = self.position
        return Vector(point[0] - x, point[1] - y)

    def abs_point(self, point: tuple) -> Vector:
        x, y = self.position
        return Vector(point[0] + x, point[1] + y)

    @property
    def display(self) -> tuple:
        w, h = self.size
        return (
            (0, 0), (0, h),
            (w, h), (w, 0)
        )

    def follow(self, position: Vector, anchor:  Anchor=Anchor.middle) -> None:
        w, h = self.size
        offs = {
            Anchor.top_left: (0, 0),
            Anchor.top: (w / 2, 0),
            Anchor.top_right: (w, 0),
            Anchor.middle_left: (0, h / 2),
            Anchor.middle: (w / 2, h / 2),
            Anchor.middle_right: (w, h / 2),
            Anchor.bottom_left: (0, h),
            Anchor.bottom: (w / 2, h),
            Anchor.bottom_right: (w, h)
        }.get(anchor, (w / 2, h / 2))
        self.position.xy = position - offs

    def set_path(self, attribute: str, path: Path, asgnmode: AssignMode, repeats: int=-1, ratio: float=0.0) -> None:
        """Adds or removes a animation path for an attribute."""
        if path is None:
            try:
                del self.paths[attribute]
            except KeyError:
                pass
        elif isinstance(path, Path):
            pth = PathState(attribute, asgnmode, path)
            pth.counter = repeats
            pth.ratio = ratio
            self.paths[attribute] = pth
        else:
            raise TypeError("'path' argument is not a Path subclass.")

    def set_smooth_transition(self, origin: Vector, destination: Vector) -> None:
        pass

    def translate(self, motion: Vector) -> 'self':
        super(View, self).translate(motion)

    def animate(self, game: type) -> None:
        """Updates animation attributes."""
        motion = self.motion * 1.0
        # check for animations
        for name in self.__dict__:
            if name not in self.paths:
                continue

            pathstate = self.paths[name]

            if pathstate.is_animating:
                ended = pathstate.animate()
                if pathstate.asgnmode is AssignMode.direct_value:
                    setattr(self, name, pathstate.position)
                elif pathstate.asgnmode is AssignMode.vector_updt:
                    getattr(self, name).xy = pathstate.position
                if ended:
                    self.on_animation_end(name, pathstate, game, self.room)

        for parallax in self.parallaxes:
            motion *= 0.75
            parallax.update(motion)

    def on_animation_end(self, attr: str, pathstate: PathState, game: type, room: 'Room'):
        pass

    def render(self, surface: pygame.Surface) -> None:
        for parallax in self.parallaxes:
            parallax.render(surface, c.BLEND_ADD)


class Room(object):

    @classmethod
    def get_command(cls, event) -> tuple or None:
        if event.type == c.KEYDOWN:
            ctrl = event.mod & c.KMOD_LCTRL or event.mod & c.KMOD_RCTRL
            alt = event.mod & c.KMOD_LALT or event.mod & c.KMOD_RALT
            shift = event.mod & c.KMOD_LSHIFT or event.mod & c.KMOD_RSHIFT

            if ctrl:
                if alt:
                    return c.K_LCTRL, c.K_LALT, event.key
                elif shift:
                    return c.K_LCTRL, c.K_LSHIFT, event.key
                else:
                    return c.K_LCTRL, event.key
            elif alt:
                if shift:
                    return c.K_LALT, c.K_LSHIFT, event.key
                else:
                    return c.K_LALT, event.key
            elif shift:
                return c.K_LSHIFT, event.key
            else:
                return (event.key,)

        return None

    def __init__(self, actors: list):
        self.actors = []
        self.visible = []
        self.minimum = Vector.zero()
        self.maximum = Vector.one()
        self.view = View(self)
        self.add_actors(actors)

    def add_actors(self, actors: list) -> None:
        for actor in actors:
            if actor not in self.actors:
                self.actors.append(actor)

    def clear(self) -> None:
        del self.actors[:]

    def update(self, events: list, keys: tuple, view: 'View', game: type) -> None:
        """Updates all objects."""
        indices = range(len(self.actors))

        # events
        for event in events:
            if event.type == c.KEYDOWN:
                cmd = Room.get_command(event)
                for i in indices:
                    self.actors[i].on_command(cmd, game, self)

            elif event.type == c.KEYUP:
                for i in indices:
                    self.actors[i].on_keyup(event.key, game, self)

            elif event.type == c.MOUSEMOTION:
                rpos = Vector(*event.pos)
                apos = self.view.abs_point(event.pos)
                rel = Vector(*event.rel)
                for i in indices:
                    self.actors[i].on_mouse_move(apos, rpos, rel, game, self)

            elif event.type == c.MOUSEBUTTONDOWN:
                rpos = Vector(*event.pos)
                apos = self.view.abs_point(event.pos)
                for i in indices:
                    {
                        1: self.actors[i].on_left_click,
                        2: self.actors[i].on_middle_click,
                        3: self.actors[i].on_right_click,
                        4: self.actors[i].on_roll_up,
                        5: self.actors[i].on_roll_down,
                    }[event.button](apos, rpos, game, self)

        # motion
        self.view.animate(game)
        for i in indices:
            self.actors[i].on_keydown(keys, game, self)
            self.actors[i].animate(game)
            self.actors[i].update(view)

        # collision
        for j in indices:
            a = self.actors[j]
            for k in indices[j + 1:]:
                b = self.actors[k]

                info = a.collide_with(b)
                BitmapFont.set_colors(BitmapFont.small, (0, 0, 0), (255, 255, 255))
                BitmapFont.render(
                    pygame.display.get_surface(),
                    "{}".format(list(info.values())),
                    BitmapFont.small,
                    Vector(0, 300)
                )

                if info[SAT.overlapped]:
                    a.on_collision(b, info, game, self)
                    b.on_collision(a, info, game, self)

        # select visible
        for actor in self.actors:
            info = self.view.collide_with(actor)
            if info[SAT.overlapped]:
                if actor not in self.visible:
                    self.visible.append(actor)
                    actor.on_enter_view(self.view, game, self)
            else:
                if actor in self.visible:
                    self.visible.remove(actor)
                    actor.on_leave_view(self.view, game, self)

        for actor in self.actors:
            actor.on_prerender(game, self)