__author__ = 'Jorge'


from enum import Enum
import pygame
import pygame.gfxdraw
import math
from spacegame.geometry import *
from spacegame.vectors import Vector
# from spacegame.core import resource

__all__ = [
    "AssignMode",
    "SAT",
    "SAT_NO_COLLISION",
    "PathState",
    "Path",
    "Path1d",
    "Path2d",
    "PathCircle",
    "Parallax",
    "Polygon",
    "Circle"
]


class AssignMode(Enum):

    direct_value = 0
    vector_updt = 1


class SAT(Enum):
    overlapped = 0
    sep_axis = 1


SAT_NO_COLLISION = {SAT.overlapped: False, SAT.sep_axis: None}


class PathState(object):

    __slots__ = ("attr", "asgnmode", "path", "counter", "_ratio", "_step", "_steps")

    def __init__(self, attr: str, asgnmode: AssignMode, path: Path) -> 'PathState':
        self.attr = attr
        self.asgnmode = asgnmode
        self.path = path
        self.counter = -1
        self._ratio = 0.0
        self._step = 0
        self._steps = 60

    @property
    def ratio(self) -> float:
        """Gets or sets the ratio of this PathState."""
        return self._ratio

    @ratio.setter
    def ratio(self, value) -> None:
        self._ratio = value % 1.0

    @property
    def length(self) -> float:
        """Gets or sets the ratio based on the path's length."""
        return self.path.get_length(self._ratio)

    @length.setter
    def length(self, value) -> None:
        self._ratio = self.path.get_ratio(value)

    @property
    def position(self) -> float or Vector:
        """Gets the position in the path."""
        return self.path.get_position(self._ratio)

    @property
    def is_animating(self) -> bool:
        """Gets whether this path state animation hasn't stopped."""
        return not (self._step == self._steps and self.counter == 0)

    def set_animation(self, framerate: int=60, seconds: float=1.0, repeats: int=-1) -> None:
        self.counter = repeats
        self._step = 0
        self._steps = int(framerate * seconds)

    def animate(self) -> bool:
        """An animation helper method. Returns whether the animation has ended."""

        self._ratio = self._step / float(self._steps)
        self._step += 1
        if self._step > self._steps:
            if self.counter >= 1:
                self.counter -= 1
                self._step = 0
            elif self.counter == -1:
                self._step = 0
            else:
                self._step = self._steps
                return True
        return False


class Path(object):

    def get_position(self, ratio: float) -> None:
        raise NotImplementedError("{} subclass method should be called.".format(self.__class__.__name__))

    def get_length(self, ratio: float) -> None:
        raise NotImplementedError("{} subclass method should be called.".format(self.__class__.__name__))

    def get_ratio(self, length: float) -> None:
        raise NotImplementedError("{} subclass method should be called.".format(self.__class__.__name__))


class Path1d(Path):

    __slots__ = ("values", "closed")

    def __init__(self, values, closed: bool=False):
        self.values = values
        self.closed = closed

    @property
    def length(self) -> float:
        """Gets the length of this path."""
        if len(self.values) in (0, 1):
            return 0.0

        length = 0
        for i in range(1, len(self.values)):
            length += abs(self.values[i] - self.values[i - 1])

        if self.closed:
            length += abs(self.values[0] - self.values[-1])

    def get_position(self, ratio: float) -> float:
        """Returns a position in the path relative to the ratio of its length."""
        ratio %= 1.0

        if self.length == 0.0:
            return 0.0

        if ratio == 0.0 or (self.closed and ratio == 1.0):
            return self.values[0]

        if ratio == 1.0:
            return self.values[-1]

        if len(self.values) > 1:
            limit = self.length * ratio
            dist = 0
            vals = self.closed and self.values[:-1] or self.values[:]
            for i, d in enumerate(vals):
                j = (i + 1) % len(self.values)
                if dist <= limit < dist + d:
                    rem = limit - dist
                    ratio2 = rem / d
                    return lerp1d(vals[i], vals[j], ratio2)
                dist += d

    def get_length(self, ratio: float) -> float:
        """Returns a path length relative to given ratio."""
        ratio %= 1.0
        l = self.length

        if l == 0.0 or ratio == 0.0:
            return 0.0

        if ratio == 1.0:
            return l

        return l * ratio

    def get_ratio(self, length: float) -> float:
        """Returns a value between 0 and 1 ralative to given length and this path's length."""
        length %= self.length

        return length / self.length


class Path2d(Path):

    __slots__ = ("points", "closed", "lengths")

    def __init__(self, points, closed: bool=False):
        self.points = points
        self.closed = closed
        self.lengths = []
        self.update()

    @property
    def length(self) -> float:
        """Gets the length of this path"""
        return sum(self.lengths)

    def update(self) -> float:
        """Calculates, stores and returns length of this path."""
        del self.lengths[:]
        _len = len(self.points)
        if _len > 1:
            for i in range(_len - 1):
                self.lengths.append(distance(self.points[i], self.points[i + 1]))

            if self.closed:
                self.lengths.append(distance(self.points[0], self.points[-1]))

            return sum(self.lengths)

        return 0.0

    def get_position(self, ratio: float) -> tuple:
        """Returns a position in the path relative to the ratio of its length."""
        ratio %= 1.0

        if self.length == 0:
            return 0.0, 0.0

        if ratio == 0.0 or (self.closed and ratio == 1.0):
            return self.points[0]

        if ratio == 1.0:
            return self.points[-1]

        if len(self.points) > 1:
            limit = self.length * ratio
            dist = 0
            pts = self.closed and self.lengths[:-1] or self.lengths[:]
            for i, d in enumerate(pts):
                j = (i + 1) % len(self.points)
                if dist <= limit < dist + d:
                    rem = limit - dist
                    ratio2 = rem / d
                    return lerp2d(pts[i], pts[j], ratio2)
                dist += d

    def get_length(self, ratio: float) -> float:
        """Returns a path length relative to given ratio."""
        ratio %= 1.0
        l = self.length

        if l == 0.0 or ratio == 0.0:
            return 0.0

        if ratio == 1.0:
            return l

        return l * ratio

    def get_ratio(self, length: float) -> float:
        """Returns a value between 0 and 1 ralative to given length and this path's length."""
        length %= self.length

        return length / self.length


class PathCircle(Path):

    __slots__ = ("position", "radius", "clockwise")

    def __init__(self, position: Vector, rad: float, clockwise: bool=False):
        self.position = position
        self.radius = rad
        self.clockwise = clockwise

    @property
    def length(self) -> float:
        """Returns the length of this circular path."""
        return circunference(self.radius)

    def get_position(self, ratio: float, from_angle: float=0.0) -> Vector:
        """Returns a position in this path relative to given ratio."""
        ratio %= 1.0
        ratio += from_angle / 360.0
        ratio %= 1.0
        angle = 360.0 * ratio
        return Vector.length_angle(self.radius, angle)

    def get_length(self, ratio: float) -> float:
        """Returns a path length relative to given ratio."""
        ratio %= 1.0
        return ratio * self.length

    def get_ratio(self, length: float) -> float:
        """Returns a value between 0 and 1 ralative to given length and this path's length."""
        length %= self.length
        return length / self.length


class Parallax(object):

    def __init__(self, image: pygame.Surface, scrollratio: Vector):
        self.image = image
        self.scrollratio = scrollratio
        self.scrollpos = Vector.zero()

    def scroll(self, position: Vector) -> None:
        self.scrollpos.xy = (position * self.scrollratio) % self.image.get_size()

    def render(self, surface: pygame.Surface, view: 'View') -> None:
        # NOTE: 'view' parameter refers to a spacegame.actors.View type of object.
        # View class is not present in this module namespace.
        self.scroll(view.position)
        pygame.gfxdraw.textured_polygon(surface, view.display, self.image, self.scrollpos.ix, self.scrollpos.iy)


class Shape(object):

    @staticmethod
    def find_normal_axis(vertices: list, index: int) -> Vector:
        vector1 = vertices[index]
        vector2 = vertices[index - 1]
        return (vector2 - vector1).normalize().perpend()

    @classmethod
    def poly_poly(cls, poly1: Polygon, poly2: Polygon) -> dict:
        vectors1 = poly1.points
        vectors2 = poly2.points
        if len(vectors1) == 2:
            temp = (vectors1[1] - vectors1[0]).perpend()
            round(temp)
            vectors1.append(vectors1[1] + temp)
        if len(vectors2) == 2:
            temp = (vectors2[1] - vectors2[0]).perpend()
            round(temp)
            vectors2.append(vectors2[1] + temp)

        # find vertical offset
        vector_offset = poly1.position - poly2.position

        # begin projection
        for i in range(len(vectors1)):
            axis = cls.find_normal_axis(vectors1, i)
            min1 = axis.dot(vectors1[0])
            max1 = min

            # project polygon 1
            for j in range(1, len(vectors1)):
                med = axis.dot(vectors1[j])
                min1 = min(min1, med)
                max1 = max(med, max1)

            # project polygon 2
            min2 = axis.dot(vectors2[0])
            max2 = min2
            for k in range(1, len(vectors2)):
                med = axis.dot(vectors2[k])
                min2 = min(min2, med)
                max2 = max(med, max2)

            offset = axis.dot(vector_offset)
            min1 += offset
            max1 += offset

            a = min1 - max2
            b = min2 - max1
            if a > 0 or b > 0:
                return SAT_NO_COLLISION

            return {
                SAT.overlapped: True,
                SAT.sep_axis: Vector(axis.x * (max2 - min1) * -1, axis.y * (max2 - min1) * -1)
            }

    @classmethod
    def circle_poly(cls, circle: Circle, poly: Polygon) -> dict:

        test_distance = -1
        closest_vector = None

        vector_offset = poly.position - circle.position
        vectors = poly.points

        if len(vectors) == 2:
            temp = (vectors[1] - vectors[0]).perpend()
            round(temp)
            vectors.append(vectors[1] + temp)

        # find closest vertex
        for i in range(len(vectors)):
            vec = poly.position + vectors[i]
            dist = (circle.position - vec).hypot
            if test_distance == -1 or dist < test_distance:
                test_distance = dist
                closest_vector = vec

        normal_axis = (closest_vector - circle.position).normalize()

        # project polygon's points
        min1 = normal_axis.dot(vectors[0])
        max1 = min1

        for j in range(1, len(vectors)):
            med = normal_axis.dot(vectors[j])
            min1 = min(min1, med)
            max1 = max(med, max1)

        # project the circle
        max2 = circle.radius
        min2 = -circle.radius

        offset = normal_axis.dot(vector_offset)
        min1 += offset
        max1 += offset

        a = min1 - max2
        b = min2 - max1
        if a > 0 or b > 0:
            return SAT_NO_COLLISION

        # find the normal axis for each point and project
        for i in range(len(vectors)):
            normal_axis = cls.find_normal_axis(vectors, i)
            min1 = normal_axis.dot(vectors[0])
            max1 = min1

            for j in range(1, len(vectors)):
                med = normal_axis.dot(vectors[j])
                min1 = min(min1, med)
                max1 = max(med, max2)

            max2 = circle.radius
            min2 = -circle.radius

            offset = normal_axis.dot(vector_offset)
            min1 += offset
            max1 += offset

            a = min1 - max2
            b = min2 - max1
            if a > 0 or b > 0:
                return SAT_NO_COLLISION

        return {
            SAT.overlapped: True,
            SAT.sep_axis: Vector(normal_axis.x * (max2 - min1) * -1, normal_axis.y * (max2 - min1) * -1),
        }

    @classmethod
    def circle_circle(cls, circle1: Circle, circle2: Circle) -> dict:
        rads = circle1.radius + circle2.radius
        vec = circle1.position - circle2.position

        if vec.hypot > rads ** 2:
            return SAT_NO_COLLISION

        diff = rads - vec.length
        return {
            SAT.overlapped: True,
            SAT.sep_axis: vec.scale(diff),
        }

    def update(self) -> None:
        pass

    def rotate(self, angle: float) -> 'self':
        raise NotImplementedError("{} is an abstract base class.".format(self.__class__.__qualname__))

    def translate(self, motion: Vector) -> 'self':
        raise NotImplementedError("{} is an abstract base class.".format(self.__class__.__qualname__))

    def scale(self, size: Vector) -> 'self':
        raise NotImplementedError("{} is an abstract base class.".format(self.__class__.__qualname__))


class Polygon(Shape):

    def __init__(self, position: Vector, rotation: float, scale: Vector, refpoints: list):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.refpoints = refpoints
        self.points = [Vector(*point) for point in refpoints]
        self.update()

    def update(self) -> None:
        """Performs rotation and scaling on points."""
        rad = math.radians(self.rotation)
        cos = math.cos(rad)
        sin = math.sin(rad)
        for i, point in enumerate(self.refpoints):
            self.points[i].fast_rotated(point, cos, sin).rescale(self.scale)

    def rotate(self, angle: float) -> 'self':
        self.rotation = (self.rotation + angle) % 360.0
        return self

    def translate(self, motion: Vector) -> 'self':
        self.position += motion
        return self

    def scale(self, size: Vector) -> 'self':
        self.scale.xy = size

    def collide_with(self, other: Shape) -> dict:

        result = {
            Polygon: Polygon.poly_poly(self, other),
            Circle: Polygon.circle_poly(other, self)
        }
        return result.get(other.__class__, SAT_NO_COLLISION)


class Circle(Shape):

    def __init__(self, position: Vector, rad: float):
        self.position = position
        self.radius = rad

    def rotate(self, angle: float) -> 'self':
        return self

    def translate(self, motion: Vector) -> 'self':
        self.position += motion
        return self

    def scale(self, size: Vector) -> 'self':
        self.radius = max(abs(size.x), abs(size.y))

    def collide_with(self, other: Shape) -> dict:

        result = {
            Polygon: Polygon.circle_poly(self, other),
            Circle: Polygon.circle_circle(self, other)
        }
        return result.get(other.__class__, SAT_NO_COLLISION)
