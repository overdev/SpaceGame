__author__ = 'Jorge A. Gomes'


import math


__all__ = [
    "radius",
    "diameter",
    "circunference",
    "distance",
    "direction",
    "lengthdir",
    "lerp2d",
    "point_line_distance",
    "point_line_nearest_point",
    "line_line_intersection",
    "circle_line_intersection"
]


def dot(a, b) -> float:
    """Returns the dot product of a and b"""
    return (float(a[0]) * b[0]) + (float(a[1]) * b[1])


def cross(a, b) -> float:
    """Returns the cross product of a and b."""
    return (float(a[0]) * b[1]) - (float(a[1]) * b[0])


def radius(circunference) -> float:
    """Returns the radius of a circle with given surface length."""
    return (circunference / math.pi) / 2


def diameter(circunference) -> float:
    """Returns the diameter of a circle with given surface length."""
    return circunference / math.pi


def circunference(radius) -> float:
    """Returns the surface length of a circle with given radius."""
    return 2 * math.pi * radius


def lengthdir(direction, distance) -> tuple:
    """Returns a point at given angle and offset."""
    r = math.radians(direction)
    return (math.cos(r) * distance, math.sin(r) * distance)


def distance(a, b, fast=False) -> float:
    """Returns de length between points a and b."""
    d = (float(b[0] - a[0]) ** 2) + (float(b[1] - a[1]) ** 2)
    if fast:
        return d

    return math.sqrt(d)


def direction(a, b) -> float:
    """Returns the angle of a pointing to b."""
    dx = b[0] - a[0]
    dy = a[1] - b[1]

    return math.degrees(math.atan2(dy, dx))


def lerp2d(a, b, r) -> tuple:
    """Returns a point interpolated from a to b, at r."""
    return (
        a[0] + (b[0] - a[0]) * r,
        a[1] + (b[1] - a[1]) * r
    )


def point_line_distance(p1, l1, l2) -> float:
    """Returns the smallest distance between line (l1, l2) and p1."""

    a = float(p1[0] - l1[0])
    b = float(p1[1] - l1[1])
    c = float(l2[0] - l1[0])
    d = float(l2[1] - l1[1])

    dotprod = a * c + b * d
    len_sq = c * c + d * d
    param = -1

    if len_sq != 0:
        # in case of 0 length line
        param = dotprod / len_sq

    if param < 0:
        xx, yy = l1

    elif param > 1:
        xx, yy = l2

    else:
        xx = l1[0] + param * c
        yy = l1[1] + param * d

    dx = (p1[0] - xx) ** 2
    dy = (p1[1] - yy) ** 2

    return math.sqrt(dx + dy)


def point_line_nearest_point(p1, l1, l2) -> tuple:
    """Returns a point in line (l1, l2) that is closest to p1."""

    a = float(p1[0] - l1[0])
    b = float(p1[1] - l1[1])
    c = float(l2[0] - l1[0])
    d = float(l2[1] - l1[1])

    dotprod = a * c + b * d
    len_sq = c * c + d * d
    param = -1

    # in case of 0 length line
    if len_sq != 0:
        param = dotprod / len_sq

    if param < 0:
        return l1

    elif param > 1:
        return l2

    return (l1[0] + param * c, l1[1] + param * d)


def line_line_intersection(a1, a2, b1, b2) -> tuple or None:
    """Returns the point of intersection between lines (a1, a2) and (b1, b2)."""
    denom = float(((b2[1] - b1[1]) * (a2[0] - a1[0])) - ((b2[0] - b1[0]) * (a2[1] - a1[1])))

    if denom == 0:
        return None

    ua = (((b2[0] - b1[0]) * (a1[1] - b1[1])) - ((b2[1] - b1[1]) * (a1[0] - b1[0]))) / denom
    ub = (((a2[0] - a1[0]) * (a1[1] - b1[1])) - ((a2[1] - a1[1]) * (a1[0] - b1[0]))) / denom

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return lerp2d(a1, a2, ua)

    return None


def circle_line_intersection(l1, l2, c1, r) -> tuple or None:
    """Returns the point(s) of intersection between line (l1, l2) and
    circle (c1, r)."""

    p1 = (l1[0] - c1[0], l1[1] - c1[1])
    p2 = (l2[0] - c1[0], l2[1] - c1[1])
    p3 = (p2[0] - p1[0], p2[1] - p1[1])

    a = float((p3[0] ** 2) + (p3[1] ** 2))
    b = float(2 * (p3[0] * p1[0]) + (p3[1] * p1[1]))
    c = float((p1[0] ** 2) + (p1[1] ** 2) - (r * r))

    delta = b * b - (4 * a * c)

    if delta < 0:
        return None

    elif delta == 0:
        u = -b / (2 * a)
        return lerp2d(l1, p3, u)

    elif delta > 0:
        sqrt_delta = math.sqrt(delta)

        u1 = (-b + sqrt_delta) / (2 * a)
        u2 = (-b - sqrt_delta) / (2 * a)

        return lerp2d(l1, p3, u1), lerp2d(l1, p3, u2)
