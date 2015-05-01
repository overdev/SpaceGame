__author__ = 'Jorge'


import math
import random


__all__ = [
    "Vector"
]


class Vector(object):

    """Specialized 2d vector class."""

    __slots__ = ('x', 'y')

    @classmethod
    def zero(cls):
        """Alternative constructor."""
        return cls(0.0, 0.0)

    @classmethod
    def one(cls):
        """Alternative constructor."""
        return cls(1.0, 1.0)

    @classmethod
    def random(cls):
        """Alternative constructor."""
        return cls(random.random(), random.random())

    @classmethod
    def normal(cls, angle):
        """Alternative constructor."""
        rad = math.radians(angle)
        return cls(math.cos(rad), math.sin(rad))

    @classmethod
    def randnormal(cls):
        """Alternative constructor."""
        rad = math.radians(random.random() * 360.0)
        return cls(math.cos(rad), math.sin(rad))

    @classmethod
    def length_angle(cls, length, angle):
        """Alternative constructor."""
        v = cls.normal(angle)
        v.x *= length
        v.y *= length
        return v

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "({:.4f}, {:.4f})".format(self.x, self.y)

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.__class__.__qualname__, self.x, self.y)

    def __getitem__(self, key) -> float or tuple:
        return [self.x, self.y][key]

    def __setitem__(self, key, value) -> None:
        [self.x, self.y][key] = value

    def __len__(self) -> int:
        return 2

    def __add__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other):
        return Vector(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        return Vector(self.x - other[0], self.y - other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return Vector(self.x * other[0], self.y * other[1])

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return Vector(other[0] * self.x, other[1] * self.y)

    def __imul__(self, other):
        if isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            return self
        self.x *= other[0]
        self.y *= other[1]
        return self

    def __truediv__(self, other):
        return Vector(self.x / other[0], self.y / other[1])

    def __rtruediv__(self, other):
        return Vector(other[0] / self.x, other[1] / self.y)

    def __itruediv__(self, other):
        self.x /= other[0]
        self.y /= other[1]
        return self

    def __floordiv__(self, other):
        return Vector(self.x // other[0], self.y // other[1])

    def __rfloordiv__(self, other):
        return Vector(other[0] // self.x, other[1] // self.y)

    def __ifloordiv__(self, other):
        self.x //= other[0]
        self.y //= other[1]
        return self

    def __mod__(self, other):
        return Vector(self.x % other[0], self.y % other[1])

    def __rmod__(self, other):
        return Vector(other[0] % self.x, other[1] % self.y)

    def __imod__(self, other):
        self.x %= other[0]
        self.y %= other[1]
        return self

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y

    def __pos__(self):
        self.x = +self.x
        self.y = +self.y

    def __abs__(self):
        self.x = abs(self.x)
        self.y = abs(self.y)

    def __invert__(self):
        self.x = ~self.x
        self.y = ~self.y

    def __round__(self, n=None):
        self.x = round(self.x, n)
        self.y = round(self.y, n)

    def __eq__(self, other):
        if other is self:
            return True
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        if other is not self:
            return False
        return self.x != other[0] or self.y != other[1]

    def __bool__(self):
        return True

    @property
    def xy(self) -> tuple:
        """Gets or sets the x,y attributes of this vector."""
        return self.x, self.y

    @xy.setter
    def xy(self, value):
        self.x, self.y = float(value[0]), float(value[1])

    @property
    def ix(self) -> int:
        return int(self.x)

    @property
    def iy(self) -> int:
        return int(self.y)

    @property
    def ixy(self):
        return self.ix, self.iy

    @property
    def point(self) -> tuple:
        """Returns a 2-tuple with x,y values truncated."""
        return int(self.x), int(self.y)

    @property
    def hypot(self) -> float:
        """Gets the hypotenuse."""
        return (self.x ** 2) + (self.y ** 2)

    @property
    def length(self) -> float:
        """Gets the length of this vector"""
        return math.sqrt(self.hypot)

    @property
    def angle(self) -> float:
        """Returns the angle of this vector."""
        return math.degrees(math.atan2(self.y, self.x))

    @property
    def normalized(self):
        """Returns the unit length of this vector."""
        length = self.length
        if length != 0:
            return Vector(self.x / length, self.y / length)
        return Vector.zero()

    def reset(self) -> 'self':
        """Sets the component values to zero."""
        self.x = 0.0
        self.y = 0.0

        return self

    def normalize(self) -> 'self':
        """Sets this vector length to one."""
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        else:
            self.reset()

        return self

    def perpend(self) -> 'self':
        """Rotates 90 degrees clockwise."""
        x, y = self
        self.x = -y
        self.y = x

        return self

    def perpend_left(self) -> 'self':
        x, y = self
        self.x = -y
        self.y = x

        return self

    def perpend_right(self) -> 'self':
        x, y = self
        self.x = y
        self.y = -x

        return self

    def rotate(self, angle) -> 'self':
        """Rotates this vector by a given angle."""
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        x, y = self
        self.x = -(cos * x - sin * y)
        self.y = sin * x + cos * y

        return self

    def translated(self, motion: 'Vector') -> 'self':
        self.x += motion[0]
        self.y += motion[1]

        return self

    def fast_rotate(self, cos, sin) -> 'self':
        x, y = self
        self.x = -(cos * x - sin * y)
        self.y = sin * x + cos * y

        return self

    def fast_rotated(self, other: object, cos, sin) -> 'self':
        x, y = other
        self.x = -(cos * x - sin * y)
        self.y = sin * x + cos * y

        return self

    def rescale(self, scalar: 'tuple or Vector') -> 'self':
        self.x *= scalar[0]
        self.y *= scalar[1]

        return self

    def rescaled(self, point, scalar: 'sequence') -> 'self':
        self.x = point[0] * scalar[0]
        self.y = point[1] * scalar[1]

        return self

    def scale(self, scalar: float) -> 'self':
        """Scales this vector by scalar ammount."""
        self.x *= scalar
        self.y *= scalar

        return self

    def dot(self, other) -> float:
        """Returns the dot product of this and other vector."""
        return (self.x * other[0]) + (self.y * other[1])

    def cross(self, other) -> float:
        """Returns the cross product of this and other vector."""
        return (self.x * other[1]) - (self.y[1] * other[0])

    def project(self, other) -> 'Vector':
        """Returns the projection of this vector onto other vector."""
        mag = (other[0] ** 2) + (other[1] ** 2)
        dotp = self.dot(other)
        scalar = dotp / mag
        return Vector(other[0] * scalar, other[1] * scalar)

    def reflect(self, normal) -> 'Vector':
        """Returns the reflection of this vector inciding on line with given normal."""
        # r = i - (2 * n * dot(i, n))
        i = self
        n = normal
        r = i - (2 * n * i.dot(n))
        return r

    def negate(self) -> 'Vector':
        return Vector(-self.x, -self.y)

    def interpolate(self, other, ratio) -> 'Vector':
        """Returns the linar interpolation between this and onther vector."""
        return Vector(
            self.x + (other[0] - self.x) * ratio,
            self.y + (other[1] - self.x) * ratio
        )

    def max(self, other):
        """Returns a vector with the maximum of x,y values."""
        return Vector(
            max(self.x, other[0]),
            max(self.y, other[1])
        )

    def min(self, other):
        """Returns a vector with the maximum of x,y values."""
        return Vector(
            min(self.x, other[0]),
            min(self.y, other[1])
        )

    def med(self, maximum, minimum):
        """Returns a vector that does not exceeds min and max values."""
        return Vector(
            max(minimum[0], min(self.x, maximum[0])),
            max(minimum[1], min(self.y, maximum[1]))
        )
