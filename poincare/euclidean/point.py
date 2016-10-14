
from __future__ import division
import math
from numbers import Real
from collections import namedtuple

class Point(namedtuple('Point', 'x y')):
    '''2D Euclidean point class, based on namedtuple with fields x and y.'''

    def __new__(cls, x, y):
        return super(Point, cls).__new__(cls, x, y)

    def distance(self, point):
        '''Distance between two points.'''
        return math.hypot(self.x - point.x, self.y - point.y)

    def distance_to_origin(self):
        '''Distance between point and origin'''
        return math.hypot(self.x, self.y)

    def azimuth(self):
        '''Azimuth of point relative to origin in radians.'''
        return math.atan2(self.y, self.x)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, type(self)):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Real):
            return Point(self.x * other, self.y * other)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Real):
            return type(self)(self.x / other, self.y / other)
        else:
            raise NotImplementedError

