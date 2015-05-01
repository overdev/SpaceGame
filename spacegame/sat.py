__author__ = 'Jorge'

# A Python implementation of Separating Axis Theorem

import pygame
from spacegame.vectors import Vector
from spacegame.geometry import *


__all__ = [
    # "AABB" # still deciding whether to add it or not.
    "Interval",
    "get_axes",
    "get_separating_axis"
]


class Interval(object):

    __slots__ = ("max", "min")

    def __init__(self, minimum: float, maximum: float):
        self.max = float(maximum)
        self.min = float(minimum)

    def overlaps(self, other: 'Interval') -> bool:
        assert isinstance(other, Interval)
        # !this.min > interval.max || interval.min > this.max
        return (self.min > other.max or other.min > self.max) is False

    def intersection(self, other: 'Interval') -> float:
        # return Math.min(this.max, interval.max) - Math.max(this.min, interval.min);
        if self.overlaps(other):
            return min(self.max, other.max) - max(self.min, other.min)
        return 0.0

    def clamp(self, value: float) -> float:
        return max(self.min, min(value, self.max))

"""
def get_axes(shape) -> list:
    sz = len(shape)
    axes = []
    for i in range(sz):
        p1 = Vector(*shape[i])
        p2 = shape[(i + 1) % sz]
        edge = p1 - p2
        edge.perpend().normalize()
        axes.append(edge)
    return axes


def project_shape(shape, axis) -> Interval:
    # axis must be normalized
    imin = imax = axis.dot(shape[0])
    for i in range(1, len(shape)):
        p = axis.dot(shape[i])
        if p < imin:
            imin = p
        elif p > imax:
            imax = p

    return imin, imax # Interval(imin, imax)


def get_separating_axis(shape1, shape2) -> tuple:
    axes1 = get_axes(shape1)
    axes2 = get_axes(shape2)
    #print(1, axes1, sep=',')
    #print(2, axes2, sep=',')
    overlap = float('inf')
    smallest = None
    resets = 0

    for i in range(len(axes1)):
        axis = axes1[i]
        amin, amax = project_shape(shape1, axis)
        bmin, bmax = project_shape(shape2, axis)

        # if not p1.overlaps(p2):
        #     return False, None, 0
        if (amin - bmax > 0) or (bmin - amax > 0):
            return False, None, 0

        # ovl = p1.intersection(p2)
        ovl = max(amax, bmax) - min(amin, bmin)
        if ovl < overlap:
            overlap = ovl
            smallest = axis
            resets += 1

    for i in range(len(axes2)):
        axis = axes2[i]
        amin, amax = project_shape(shape1, axis)
        bmin, bmax = project_shape(shape2, axis)

        if (amin - bmax > 0) or (bmin - amax > 0):
            return False, None, 0
        # if not p1.overlaps(p2):
        #     return False, None, 0

        #ovl = p1.intersection(p2)
        ovl = max(amax, bmax) - min(amin, bmin)
        if ovl < overlap:
            overlap = ovl
            smallest = axis
            resets += 1

    print(resets)
    return True, smallest, overlap

"""


def get_axes(poly1: list, poly2: list) -> list:
    axes = []
    for i in range(len(poly1)):
        edge = (poly1[i][0] - poly1[i - 1][0]), (poly1[i][1] - poly1[i - 1][1])
        axis = normalize(edge)
        axis = perpend_left(axis)
        axes.append(axis)

    # for i in range(len(poly2)):
    #     edge = (poly2[i][0] - poly2[i - 1][0]),(poly2[i][1] - poly2[i - 1][1])
    #     axis = normalize(edge)
    #     axis = perpend_left(axis)
    #     axes.append(axis)

    return axes


def get_projection(poly: list, axis: Vector) -> tuple:

    pmin = pmax = dot(poly[0], axis)
    for i in range(1, len(poly)):
        proj = dot(poly[i], axis)

        if proj < pmin:
            pmin = proj
        elif proj > pmax:
            pmax = proj

    return pmin, pmax


def get_separating_axis(poly1: list, poly2: list) -> dict:

    axes = get_axes(poly1, poly2)
    sep_dist = float('-inf')
    sep_axis = None

    t = 0
    for axis in axes:
        amin, amax = get_projection(poly1, axis)
        bmin, bmax = get_projection(poly2, axis)
        ax = Vector(*axis)
        pygame.draw.line(pygame.display.get_surface(), (192, 32, 32), (ax * amin)+(400,300), (ax*amax)+(400,300))
        pygame.draw.line(pygame.display.get_surface(), (32, 32, 192), (ax * bmin)+(400,300), (ax*bmax)+(400,300))
        t += 1

        dist = max(amin, bmin) - min(bmax, amax)
        # dist =  max(bmin, amin) - min(amax, bmax)
        if (amax < bmin) or (bmax < amin):
            return {
                0: False,
                1: Vector(*axis),
                2: dist
            }

        if 0 > dist > sep_dist:
            sep_dist = dist
            sep_axis = axis

    return {
        0: True,
        1: Vector(*sep_axis),
        2: sep_dist
    }
