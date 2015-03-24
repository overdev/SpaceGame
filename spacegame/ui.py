__author__ = 'Jorge'


import pygame
import types
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


def event(func):
    """Function decorator for Listener events"""
    if isinstance(func, types.MethodType):
        cls = func.__self__.__class__
        if issubclass(cls, Listener):
            name = func.__name__
            cls.handlers[name] = func
        else:
            print("'event' decorator not in Listener subclass")
    else:
        print("instance method expected.")


class Listener(object):

    """A basic event listener.

    Calls handler functions based on events triggered."""

    handlers = {}

    def __getattr__(self, name):
        if name in self.__class__.handlers:
            return self.__class__.handlers[name]
        else:
            msg = "{} object has no attribute '{}'.".format(self.__class__, name)
            raise AttributeError(msg)


class Test(Listener):

    @event
    def on_event(self):
        pass