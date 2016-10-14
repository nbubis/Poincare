
import math
from poincare.euclidean.point import Point
from poincare.euclidean.line import Line
from poincare.euclidean.circle import Circle


class HyperbolicLine(object):
    '''Class for lines in hyperblic space, as represented by the Poincare Disk Model'''

    def __init__(self, point_a, point_b):
        '''Constructs a HyperbolicLine between two Points.'''
        if not point_a.isvalid() or not point_b.isvalid():
            raise ValueError
        # k (x^2 + y^2) - 2 x0 x - 2 y y0 + k = 0
        # k = 1:
        # (x - x0)^2 + (y - y0)^2 = (x0^2 + y0^2 - 1)
        # k = 0:
        # y0 y + x0 x = 0
        self._is_a_stright_line = False
        dist_to_origin = Line(point_a, point_b).distance_to_origin()
        if dist_to_origin < 10e-9:
            self._is_a_stright_line = True
            if point_a.distance_to_origin() > point_b.distance_to_origin():
                self._x0, self._y0 = point_a.y, -point_a.x
            else:
                self._x0, self._y0 = point_b.y, -point_b.x
        else:
            point_c = point_a.inverse()
            circle = Circle.create_from_three_points(point_a, point_b, point_c)
            self._x0, self._y0 = circle.center

    def get_representation(self):
        if self._is_a_stright_line:
            return Line(self._x0, self._y0, 0)
        else:
            radius = math.sqrt(self._x0**2 + self._y0**2 - 1.0)
            return Circle(Point(self._x0, self._y0), radius)

    # def distance(self, other):
    #     if isinstance(other, HyperbolicPoint):
    #         if Point.distance(self, other) < 10e-9:
    #             return 0.0
    #         if abs(Line(self, other).distance_to_point(Point(0, 0))) < 10e-9:
    #             return abs(self.distance_to_origin() - other.distance_to_origin())

    #         arc_circle = self.arc_to_point(other)
    #         p, q = self, other
    #         a, b = arc_circle.intersection(self.unit_circle)
    #         if Point.distance(a, q) < Point.distance(a, p):
    #             a, b = b, a
    #         ratio = (Point.distance(a, q) * Point.distance(p, b)) / (Point.distance(a, p) * Point.distance(q, b))
    #         return math.log(ratio)

    #     else:
    #         raise NotImplementedError
