
import math
from numbers import Real
from collections import namedtuple
from poincare.euclidean.point import Point

class Line(namedtuple('Line', 'a b c')):
    '''2D Euclidean line class, based on namedtuple with fields a, b and c.
       Creates a line of the form a*x + b*y = c'''

    def __new__(cls, *kargs):
        '''Allows creating a line from the three parameters, two Points, or a single tuple of length three.'''
        if len(kargs) == 3 and all(isinstance(i, Real) for i in kargs):
            return super(Line, cls).__new__(cls, *kargs)

        elif len(kargs) == 2 and all(isinstance(i, Point) for i in kargs):
            x1, y1 = kargs[0].x, kargs[0].y
            x2, y2 = kargs[1].x, kargs[1].y
            return super(Line, cls).__new__(cls, *(y2 - y1, x1 - x2, x1 * (y2 - y1) - y1 * (x2 - x1)))

        elif len(kargs) == 1 and isinstance(kargs[0], tuple) and len(kargs[0]) == 3:
            return super(Line, cls).__new__(cls, *kargs[0])

        else:
            raise NotImplementedError

    def distance_to_point(self, point):
        '''Returns distance between the current Line and a Point.'''
        if not isinstance(point, Point):
            raise NotImplementedError
        orthogonal_line = self.orthogonal_line_at_point(point)
        intersection_point = self.intersection(orthogonal_line)
        return point.distance(intersection_point)

    def distance_to_origin(self):
        '''Returns distance between the current Line and the origin.'''
        return self.distance_to_point(Point(0, 0))

    def orthogonal_line_at_point(self, point):
        '''Returns a new Line orthogonal to the current Line.'''
        return Line(-self.b, self.a, self.a * point.y - self.b * point.x)

    def intersection(self, other):
        '''Returns the intersection Point between lines.'''
        if isinstance(other, Line):
            a1, b1, c1 = self
            a2, b2, c2 = other

            x_intersect = (c2 * b1 - b2 * c1) / (a2 * b1 - b2 * a1)
            if abs(b2) > abs(b1):
                y_intersect = (c2 - a2 * x_intersect) / b2
            else:
                y_intersect = (c1 - a1 * x_intersect) / b1
            return Point(x_intersect, y_intersect)

        else:
            raise NotImplementedError

    def angle_between(self, other):
        '''Returns angle in radians between two Lines, between 0 and pi'''
        if not isinstance(other, Line):
            raise NotImplementedError
        a1, a2, b1, b2 = self.a, other.a, self.b, other.b
        dot_product = (a1 * a2 + b1 * b2) / math.sqrt((a1**2 + b1**2) * (a2**2 + b2**2))
        return math.acos(dot_product)


        