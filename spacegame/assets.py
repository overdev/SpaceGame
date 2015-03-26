__author__ = 'Jorge'


from spacegame.geometry import *
from spacegame.vectors import Vector

__all__ = [

]


class PolyPath(object):

    __slots__ = ("points", "closed", "lengths")

    def __init__(self, points, closed=False):
        self.points = points
        self.closed = closed
        self.lengths = []
        self.update()

    @property
    def length(self):
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

    def get_position(self, ratio: float) -> Vector:
        """Returns a position in the path relative to the ratio of its length."""
        ratio %= 1.0

        if self.length == 0:
            return Vector.zero()

        if ratio == 0.0 or (self.closed and ratio == 1.0):
            return Vector(*self.points[0])

        if ratio == 1.0:
            return Vector(*self.points[-1])

        if len(self.points) > 1:
            limit = self.length * ratio
            dist = 0
            pts = self.closed and self.lengths[:-1] or self.lengths[:]
            for i, d in enumerate(pts):
                j = (i + 1) % len(self.points)
                if dist <= limit < dist + d:
                    rem = limit - dist
                    ratio2 = rem / d
                    return Vector(*lerp2d(pts[i], pts[j], ratio2))
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


class CircularPath(object):

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
