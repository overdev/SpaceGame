__author__ = 'Jorge'


import pygame
import pygame.locals as c
from .core import resource
from .geometry import Vec

__all__ = [
    "BitmapFont",
    "blend_color"
]

# BmpFont constants
BMP = 0     # the resource surface
PAL = 1     # a copy of the default palette (a sequence of 4-int tuples)
NRM = 2     # a normalized palette (a sequence of 3-float tuples)
CEL = 3     # the tile size (w, h)
GRD = 4     # the tile grid size (w, h)
GLY = 5     # the glyph position and size in the tile region (x, y, w, h)
CHR = 6     # the characters contained in the font (a string)
BFC = 7     # the current background and foreground colors wich the surface palette was blended into


def normalize_color(color) -> tuple:
    """Normalizes the components of the given color."""
    return (
        color[0] / 255.0,
        color[1] / 255.0,
        color[2] / 255.0
    )


def blend_color(a, b, ratio) -> tuple:
    """Blends and returns the mix of colors a and b to a given ratio.

    Note: ratio argument must be a 3-float sequence."""
    return (
        int(a[0] + (b[0] - a[0]) * ratio[0]),
        int(a[1] + (b[1] - a[1]) * ratio[1]),
        int(a[2] + (b[2] - a[2]) * ratio[2])
    )


class BitmapFont(object):

    src = pygame.image.load(resource("small_(5,2,6,12).png"))
    small = {
        BMP: src,
        PAL: src.get_palette(),
        NRM: (normalize_color(col) for col in src.get_palette()),
        CEL: (16, 16),
        GRD: (32, 7),
        GLY: (5, 2, 6, 12),
        CHR: "",
        BFC: ((0, 0, 0), (255, 255, 255))
    }
    # medium and large size fonts are yet to be done.
    del src

    @classmethod
    def set_colors(cls, font, background, foreground) -> None:
        """Set the font palette colors to given colors."""

        for index in range(256):
            color = blend_color(background, foreground, font[NRM][index])
            font[BMP].set_palette_at(color)

        font[BFC] = (background, foreground)

    @classmethod
    def get_colors(cls, font) -> tuple:
        """Returns the current background and foreground colors of the given font palette."""

        return font[BFC]

    @classmethod
    def render(cls, surface, text, font, position, blend=0) -> None:
        """Renders the given text str with the given font at the given position."""
        x, y = position
        gw = font[GLY][2]
        gh = font[GLY][3]

        for n, char in enumerate(text):
            if char in font[CHR]:
                ind = font[CHR].index(char)
            else:
                ind = 0

            # the char glyph tile x,y position in the grid
            tile = Vec.swap_xy(divmod(ind, font[GRD][0]))

            gx = (tile.x * font[CEL][0]) + font[GLY][0]
            gy = (tile.y * font[CEL][1]) + font[GLY][1]

            surface.blit(font[BMP], (x, y), (gx, gy, gw, gh), blend)

            x += gw


class UIElement(object):

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
                return event.key

        return None

    def __init__(self, position, size):
        self.pos = Vec(*position)
        self.size = Vec(*size)
        self.label = "uielmt"
        self.icon = None
        self.command = None
        self.active = True
        self.visible = True

    def contains_point(self, point) -> bool:
        """Returns whether the given point is inside this object's bounds."""
        return (self.pos.x <= point[0] <= self.pos.x + self.size.x and
                self.pos.y <= point[1] <= self.pos.y + self.size.y and
                self.visible)

    def inner_point(self, point) -> Vec:
        """Returns a point relative to this object's position."""
        return self.pos - point

    def responds_to(self, command) -> bool:
        """Returns whether this object will respond to keyboard input."""
        return command == self.command and self.active is True and self.command is not None

    def on_left_click(self, client) -> None:
        """Called when the left mouse button is pressed over this object."""
        pass

    def on_right_click(self, client) -> None:
        """Called when the right mouse button is pressed over this object."""
        pass

    def on_middle_click(self, client) -> None:
        """Called when the middle mouse button is pressed over this object."""
        pass

    def on_client_enter(self, client) -> None:
        """Called when the mouse moves in this object."""
        pass

    def on_client_move(self, client) -> None:
        """Called when the mouse moves over this object."""
        pass

    def on_client_exit(self, client) -> None:
        """Called when the mouse moves out this object."""
        pass

    def on_roll_up(self, client) -> None:
        """Called when the mouse wheel rolls up over this object."""
        pass

    def on_roll_down(self, client) -> None:
        """Called when the mouse wheel rolls down over this object."""
        pass

    def on_command(self) -> None:
        """Called when the this object's keyboard command is entered."""
        pass


class Dispatcher(object):

    def __init__(self, listeners):
        self.listeners = []
        self._mouse_listeners = []
        for listener in listeners:
            self.listeners.append(listener)

    def process_events(self, events) -> None:

        for event in events:
            if event.type == c.KEYDOWN:
                cmd = UIElement.get_command(event)
                for listener in self.listeners:
                    if listener.responds_to(cmd):
                        listener.on_command()

            elif event.type == c.MOUSEMOTION:
                for listener in self.listeners:
                    if listener.contains_point(event.pos):
                        if listener in self._mouse_listeners:
                            listener.on_client_move(listener.inner_point(event.pos))
                        else:
                            listener.on_client_enter()
                            self._mouse_listeners.append(listener)
                    else:
                        if listener in self._mouse_listeners:
                            listener.on_clent_exit()
                            self._mouse_listeners.remove(listener)

            elif event.type == c.MOUSEBUTTONDOWN:
                for listener in self._mouse_listeners:
                    if event.button == 1:
                        listener.on_left_click(listener.inner_point(event.pos))
                    elif event.button == 2:
                        listener.on_middle_click(listener.inner_point(event.pos))
                    elif event.button == 3:
                        listener.on_right_click(listener.inner_point(event.pos))
                    elif event.button == 4:
                        listener.on_roll_up(listener.inner_point(event.pos))
                    elif event.button == 5:
                        listener.on_roll_down(listener.inner_point(event.pos))