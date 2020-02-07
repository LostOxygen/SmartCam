from ..exceptions.exceptions import NoInstanceException
from sympy.geometry import Point, Point2D, Polygon, Circle
import math
import numpy as np

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        if not isinstance(v, Vector):
            return NoInstanceException(v, Vector)
        return Vector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        if not isinstance(v, Vector):
            return NoInstanceException(v, Vector)
        return Vector(self.x - v.x, self.y - v.y)

    def cross(self, v):
        if not isinstance(v, Vector):
            return NoInstanceException(v, Vector)
        return self.x*v.y - self.y*v.x

    def angle(self, v):
        if not isinstance(v, Vector):
            return NoInstanceException(v, Vector)
        return np.round(np.rad2deg(np.arccos((self.x*v.x + self.y*v.y) / (math.sqrt(self.x**2 + self.y**2) * math.sqrt(v.x**2 + v.y**2)))), 2)


class Line_():
    def __init__(self, v1, v2):
        self.a = v2.y - v1.y
        self.b = v1.x - v2.x
        self.c = v2.cross(v1)

    def __call__(self, p):
        return self.a*p.x + self.b*p.y + self.c

    def intersection(self, other): #intersection between line itself and any other line
        if not isinstance(other, Line_):
            return NoInstanceException(v, Line_)
        w = self.a*other.b - self.b*other.a

        return Vector(
            (self.b*other.c - self.c*other.b)/w,
            (self.c*other.a - self.a*other.c)/w
        )


class Area():
    def __init__(self):
        pass

    def intersection(gripPoint, box, gripArea):
        gripArea = Polygon(gripArea[0], gripArea[1], gripArea[2], gripArea[3])

        polygon_box = Polygon(box[0], box[1], box[2], box[3])

        intersections = polygon_box.intersection(gripArea)

        if len(intersections) > 0:
            return True

        return False
