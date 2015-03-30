__author__ = 'Jorge'


from enum import Enum
import pygame
import pygame.locals as c
from spacegame.core import resource
from spacegame.geometry import Vec

__all__ = [
    "BitmapFont",
    "blend_color",
    "Anchor",
    "UIElement",
    "Button",
    "Switcher",
    "List"
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


# Font alignment constants
class Anchor(Enum):
    top_left = 1
    top = 2
    top_right = 3
    middle_left = 4
    middle = 5
    middle_right = 6
    bottom_left = 7
    bottom = 8
    bottom_right = 9


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
        NRM: tuple(normalize_color(col) for col in src.get_palette()),
        CEL: (16, 16),
        GRD: (32, 7),
        GLY: (5, 2, 6, 12),
        CHR: " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~_¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ",
        BFC: ((0, 0, 0), (255, 255, 255))
    }
    src = pygame.image.load(resource("medium_(0,0,36,18).png"))
    medium = {
        BMP: src,
        PAL: src.get_palette(),
        NRM: tuple(normalize_color(col) for col in src.get_palette()),
        CEL: (16, 36),
        GRD: (32, 7),
        GLY: (0, 0, 16, 36),
        CHR: " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~_¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ",
        BFC: ((0, 0, 0), (255, 255, 255))
    }
    src = pygame.image.load(resource("large_(0,0,64,32).png"))
    large = {
        BMP: src,
        PAL: src.get_palette(),
        NRM: tuple(normalize_color(col) for col in src.get_palette()),
        CEL: (32, 64),
        GRD: (32, 7),
        GLY: (0, 0, 32, 64),
        CHR: " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~_¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ",
        BFC: ((0, 0, 0), (255, 255, 255))
    }
    del src

    @classmethod
    def set_colors(cls, font, background, foreground) -> None:
        """Set the font palette colors to given colors."""

        for index in range(256):
            color = blend_color(background, foreground, font[NRM][index])
            font[BMP].set_palette_at(index, color)

        font[BFC] = (background, foreground)

    @classmethod
    def get_colors(cls, font) -> tuple:
        """Returns the current background and foreground colors of the given font palette."""

        return font[BFC]

    @classmethod
    def measure(cls, text, font, position, anchor=Anchor.top_left) -> tuple:
        """Returns a (x, y, w, h) tuple reflecting the text bounds"""
        x, y = position
        w = font[GLY][2] * len(text)
        h = font[GLY][3]

        # faster and prettier than if/elif chains
        rct = {
            Anchor.top_left: (x, y, w, h),
            Anchor.top: (x - (w / 2), y, w, h),
            Anchor.top_right:  (x - (w / 2), y - h, w, h),
            Anchor.middle_left: (x, y - (h / 2), w, h),
            Anchor.middle: (x - (w / 2), y - (h / 2), w, h),
            Anchor.middle_right: (x - w, y - (h / 2), w, h),
            Anchor.bottom_left: (x, y - h, w, h),
            Anchor.bottom: (x - (w / 2), y - h, w, h),
            Anchor.bottom_right: (x - w, y - h, w, h)
        }

        if anchor in rct:
            return rct[anchor]
        return rct[Anchor.top_left]

    @classmethod
    def render(cls, surface, text, font, position, anchor=Anchor.top_left, blend=0) -> None:
        """Renders the given text str with the given font at the given position."""
        x, y, w, h = cls.measure(text, font, position, anchor)
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
                return (event.key,)

        return None

    def __init__(self, position, size):
        self._pos = Vec(*position)
        self._size = Vec(*size)
        self.label = "uielmt"
        self.icon = None
        self.command = None
        self.active = True
        self.visible = True
        self.hover = False

        # the initialization
        self.on_initialize()

    @property
    def pos(self):
        """Gets or sets the position of this ui element."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Vec(*value)

    @property
    def size(self):
        """Gets or sets the size of this ui element."""
        return self._size

    @size.setter
    def size(self, value):
        self._size = Vec(*value)

    def get_anchor_pos(self, anchor) -> Vec:
        """Returns a point relative to the given anchor"""
        x, y = self.pos
        w, h = self.size

        # faster and prettier than if/elif chains
        rct = {
            Anchor.top_left: Vec(x, y),
            Anchor.top: Vec(x + (w / 2), y),
            Anchor.top_right:  Vec(x + (w / 2), y + h),
            Anchor.middle_left: Vec(x, y + (h / 2)),
            Anchor.middle: Vec(x + (w / 2), y + (h / 2)),
            Anchor.middle_right: Vec(x + w, y + (h / 2)),
            Anchor.bottom_left: Vec(x, y + h),
            Anchor.bottom: Vec(x + (w / 2), y + h),
            Anchor.bottom_right: Vec(x + w, y + h)
        }

        if anchor in rct:
            return rct[anchor]
        return rct[Anchor.top_left]

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

    def on_initialize(self) -> None:
        """Called in the instance creation."""
        pass

    def on_keydown(self, keys, game) -> None:
        """Called whenever a keyboard key is down."""
        pass

    def on_left_click(self, client, game) -> None:
        """Called when the left mouse button is pressed over this object."""
        pass

    def on_right_click(self, client, game) -> None:
        """Called when the right mouse button is pressed over this object."""
        pass

    def on_middle_click(self, client, game) -> None:
        """Called when the middle mouse button is pressed over this object."""
        pass

    def on_client_enter(self, game) -> None:
        """Called when the mouse moves in this object."""
        pass

    def on_client_move(self, client, game) -> None:
        """Called when the mouse moves over this object."""
        pass

    def on_client_exit(self, game) -> None:
        """Called when the mouse moves out this object."""
        pass

    def on_roll_up(self, client, game) -> None:
        """Called when the mouse wheel rolls up over this object."""
        pass

    def on_roll_down(self, client, game) -> None:
        """Called when the mouse wheel rolls down over this object."""
        pass

    def on_command(self, game) -> None:
        """Called when the this object's keyboard command is entered."""
        pass

    def basic_render(self, surface) -> None:
        """Displays this object with default rendering"""
        if not self.visible:
            return
        l, t = self.pos
        r, b = self.get_anchor_pos(Anchor.bottom_right)
        tpos = self.get_anchor_pos(Anchor.middle)
        backcolor = (128, 128, 128)
        forecolor = {False: (255, 255, 192), True: (255, 0, 0)}
        pts = ((l, t), (r, t), (r, b), (l, b))
        pygame.draw.polygon(surface, backcolor, pts, 0)
        pygame.draw.polygon(surface, forecolor[self.hover], pts, 1)
        BitmapFont.set_colors(BitmapFont.medium, backcolor, forecolor[self.hover])
        BitmapFont.render(surface, str(self.label), BitmapFont.medium, tpos, Anchor.middle)


class Dispatcher(object):

    def __init__(self, listeners):
        self.listeners = []
        self._mouse_listeners = []
        for listener in listeners:
            self.listeners.append(listener)

        # post an mouse motion event to update objects under the mouse
        # when the scene starts
        pos = pygame.mouse.get_pos()
        rel = (0, 0)
        e = pygame.event.Event(c.MOUSEMOTION, {'pos': pos, 'rel': rel, 'buttons': (False, False, False)})
        pygame.event.post(e)

    def process_events(self, events: list, keys: tuple, game: type) -> None:

        for event in events:
            if event.type == c.QUIT:
                game.scene = None
            elif event.type == c.KEYDOWN:
                cmd = UIElement.get_command(event)
                for listener in self.listeners:
                    if listener.responds_to(cmd):
                        listener.on_command(game)

            elif event.type == c.MOUSEMOTION:
                for listener in self.listeners:
                    if listener.contains_point(event.pos):
                        if listener in self._mouse_listeners:
                            listener.on_client_move(listener.inner_point(event.pos), game)
                        else:
                            listener.hover = True
                            listener.on_client_enter(game)
                            self._mouse_listeners.append(listener)
                    else:
                        if listener in self._mouse_listeners:
                            listener.hover = False
                            listener.on_client_exit(game)
                            self._mouse_listeners.remove(listener)

            elif event.type == c.MOUSEBUTTONDOWN:
                for listener in self._mouse_listeners:
                    {
                        1: listener.on_left_click,
                        2: listener.on_middle_click,
                        3: listener.on_right_click,
                        4: listener.on_roll_up,
                        5: listener.on_roll_down
                    }[event.button](listener.inner_point(event.pos), game)

        for listener in self.listeners:
            if listener.active:
                listener.on_keydown(keys, game)


class Button(UIElement):

    def __init__(self, position, size, label, icon):
        super(Button, self).__init__(position, size)
        self.label = label
        self.icon = icon


class Switcher(UIElement):

    def __init__(self, position, size, modes, mode):
        super(Switcher, self).__init__(position, size)
        self.label = mode
        self.modes = modes


class List(UIElement):

    def __init__(self, position, size, items):
        super(List, self).__init__(position, size)
        self.items = items
        self.item = None
