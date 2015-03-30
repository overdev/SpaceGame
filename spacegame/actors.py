__author__ = 'Jorge'


import pygame
import pygame.locals as c
from spacegame.geometry import *
from spacegame.vectors import Vector
from spacegame.assets import *
from spacegame.ui import Anchor


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

    def on_animation_end(self, attr: str, pathstate: PathState, game: type):
        """Called when the animation for the attribute reaches the last step."""

    def on_collision(self, other: 'Actor', info: dict, game: type):
        """Called when this object collides with other."""
        pass

    def on_keydown(self, keys: tuple, game: type) -> None:
        """Called whenever a keyboard key is down."""
        pass

    def on_left_click(self, screen: tuple, game: type) -> None:
        """Called when the left mouse button is pressed."""
        pass

    def on_right_click(self, screen, game) -> None:
        """Called when the right mouse button is pressed."""
        pass

    def on_middle_click(self, screen, game) -> None:
        """Called when the middle mouse button is pressed."""
        pass

    def on_mouse_move(self, room_pos:Vector, view_pos: Vector, motion: Vector, game: type) -> None:
        """Called when the mouse moves over this object."""
        pass

    def on_client_exit(self, game) -> None:
        """Called when the mouse moves out this object."""
        pass

    def on_roll_up(self, client, game) -> None:
        """Called when the mouse wheel rolls up."""
        pass

    def on_roll_down(self, client, game) -> None:
        """Called when the mouse wheel rolls down."""
        pass

    def on_enter_view(self, view: 'View', game: type) -> None:
        """Called when the object gets partially or totally inside the view area."""

    def on_leave_view(self, view: 'View', game: type) -> None:
        """Called when the object get totally outside the view area."""

    def on_command(self, cmd: tuple, game: type) -> None:
        """Called when the this object's keyboard command is entered."""
        pass


class View(Polygon):

    refpoints = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    transition = Path1d([0.75 ** i for i in range(20)])

    def __init__(self, room: 'Room'):
        super(View, self).__init__(Vector.zero(), 0.0, Vector(*self.size), View.refpoints)
        self.room = room
        self.anchor = Anchor.top_left
        self.paths = {}
        self.set_path('transition', View.transition, AssignMode.direct_value, 0)

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
            (0, 0), (0, w),
            (h, w), (h, 0)
        )

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
                    self.on_animation_end(name, pathstate, game)

    def on_animation_end(self, attr: str, pathstate: PathState, game: type):
        pass


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
                    self.actors[i].on_command(cmd, game)

            elif event.type == c.MOUSEMOTION:
                rpos = Vector(*event.pos)
                apos = self.view.abs_point(event.pos)
                rel = Vector(*event.rel)
                for i in indices:
                    self.actors[i].on_mouse_move(apos, rpos, rel, game)

        # motion
        self.view.animate(game)
        for i in indices:
            self.actors[i].on_keydown(keys, game)
            self.actors[i].animate(game)
            self.actors[i].update(view)

        # collision
        for j in indices:
            a = self.actors[j]
            for k in indices[j + 1:]:
                b = self.actors[k]

                info = a.collides_with(b)
                if info[SAT.overlapped]:
                    a.on_collision(b, info, game)
                    b.on_collision(a, info, game)

        # select visible
        for actor in self.actors:
            info = self.view.collide_with(actor)
            if info[SAT.overlapped]:
                if actor not in self.visible:
                    self.visible.append(actor)
                    actor.on_enter_view(self.view, game)
            else:
                if actor in self.visible:
                    self.visible.remove(actor)
                    actor.on_leave_view(self.view, game)

