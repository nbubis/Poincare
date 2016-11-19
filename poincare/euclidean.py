'''Module containing Euclidean constructions, Poine, Line and Circle.'''

import math
from numbers import Real
from collections import namedtuple

class Point(namedtuple('Point', 'x y')):
    '''2D Euclidean point class, based on a namedtuple with fields x and y.'''

    def __new__(cls, x, y):
        return super().__new__(cls, x, y)

    def distance(self, point):
        '''Distance between two points.'''
        return math.hypot(self.x - point.x, self.y - point.y)

    def distance_to_origin(self):
        '''Distance between point and origin'''
        return math.hypot(self.x, self.y)

    def azimuth(self):
        '''Azimuth of point relative to origin in radians.'''
        return math.atan2(self.y, self.x)

    def rotated_point(self, anchor, angle):
        '''Return the point's location after rotation by the angle around an anchor point.'''
        difference = self - anchor
        rotated = Point(difference.x * math.cos(angle) - difference.y * math.sin(angle) + anchor.x,
                        difference.x * math.sin(angle) + difference.y * math.cos(angle) + anchor.y)
        return rotated

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, type(self)):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Real):
            return type(self)(self.x * other, self.y * other)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Real):
            return type(self)(self.x / other, self.y / other)
        else:
            raise NotImplementedError


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

    def intersection(self, other):
        '''Returns list of intersection points between the circle and other lines or circles.'''
        if isinstance(other, Line):
            return _line_line_intersection(self, other)
        elif isinstance(other, Circle):
            return _circle_line_intersection(other, self)
        else:
            raise NotImplementedError

    def distance_to_point(self, point):
        '''Returns distance between the current Line and a Point.'''
        orthogonal_line = self.orthogonal_line_at_point(point)
        intersection_point = _line_line_intersection(self, orthogonal_line)[0]
        return point.distance(intersection_point)

    def distance_to_origin(self):
        '''Returns distance between the current Line and the origin.'''
        return self.distance_to_point(Point(0, 0))

    def orthogonal_line_at_point(self, point):
        '''Returns a new Line orthogonal to the current Line.'''
        return Line(-self.b, self.a, self.a * point.y - self.b * point.x)

    def rotated_line(self, anchor, angle):
        '''Returns a line rotated counter clockwise by the given angle around an anchor point.'''
        a, b, c = self
        if abs(a) > abs(b):
            point_a, point_b = Point(c / a, 0), Point((c - b) / a, 1)
        else:
            point_a, point_b = Point(0, c / b), Point(1, (c - a) / b)

        point_a, point_b = point_a.rotated_point(anchor, angle), point_b.rotated_point(anchor, angle)
        return Line(point_a, point_b)

    def angle_between(self, other):
        '''Returns angle in radians between two Lines, between 0 and pi'''
        a1, a2, b1, b2 = self.a, other.a, self.b, other.b
        dot_product = (a1 * a2 + b1 * b2) / math.sqrt((a1**2 + b1**2) * (a2**2 + b2**2))
        return math.acos(dot_product)


class Circle(object):
    '''Class for euclidean circle objects.'''

    def __init__(self, center, radius):
        '''Constructs a Circle using a center Point and the radius.'''
        self.center, self.radius = center, radius

    def intersection(self, other):
        '''Returns list of intersection points between the circle and other lines or circles.'''
        if isinstance(other, Line):
            return _circle_line_intersection(self, other)
        elif isinstance(other, Circle):
            return _circle_circle_intersection(self, other)
        else:
            raise NotImplementedError

    @staticmethod
    def create_from_three_points(point_a, point_b, point_c):
        '''Returns Circle passing through three Points.'''
        points_list = [point_a, point_b, point_c]
        points_cycles = [points_list[i:] + points_list[:i] for i in range(len(points_list))]
        denominator = 2.0 * sum(a.x * (b.y - c.y) for a, b, c in points_cycles)
        center_x = sum((a.x**2 + a.y**2) * (b.y - c.y) for a, b, c in points_cycles) / denominator
        center_y = sum((a.x**2 + a.y**2) * (c.x - b.x) for a, b, c in points_cycles) / denominator
        center = Point(center_x, center_y)
        return Circle(center, (center - point_a).distance_to_origin())

    def angle_between(self, other):
        '''Returns angle in radians between two Circles, between 0 and pi'''
        intersection_pt = self.intersection(other)[0]
        lines_to_centers = [Line(intersection_pt, self.center), Line(intersection_pt, other.center)]
        return lines_to_centers[0].angle_between(lines_to_centers[1])


def _circle_circle_intersection(circle1, circle2):
    '''Returns list of intersection points between the circle and circles.'''
    x0, y0, r0 = circle1.center.x, circle1.center.y, circle1.radius
    x1, y1, r1 = circle2.center.x, circle2.center.y, circle2.radius

    center_distance_sq = (x0 - x1)**2 + (y0 - y1)**2
    x_intersection_first_term = 0.5 * (x0 + x1) + 0.5 * (x0 - x1)*(r1**2 - r0**2) / center_distance_sq
    y_intersection_first_term = 0.5 * (y0 + y1) + 0.5 * (y0 - y1)*(r1**2 - r0**2) / center_distance_sq

    try:
        x_intersection_second_term = 0.5 * (y1 - y0) / center_distance_sq * \
            math.sqrt(((r1 + r0)**2 - center_distance_sq) * (center_distance_sq - (r1 - r0)**2))
        y_intersection_second_term = 0.5 * (x1 - x0) / center_distance_sq * \
            math.sqrt(((r1 + r0)**2 - center_distance_sq) * (center_distance_sq - (r1 - r0)**2))

        point1 = Point(x_intersection_first_term + x_intersection_second_term,
                       y_intersection_first_term - y_intersection_second_term)
        point2 = Point(x_intersection_first_term - x_intersection_second_term,
                       y_intersection_first_term + y_intersection_second_term)
        return [point1, point2]

    except ValueError:
        return []

def _circle_line_intersection(circle, line):
    '''Returns list of intersection points between the circle and other lines.'''
    x0, y0, r0 = circle.center.x, circle.center.y, circle.radius
    a, b, c = line.a, line.b, line.c

    try:
        c = c - a * x0 - b * y0
        root_term = math.sqrt(r0**2 * (a**2 + b**2) - c**2) / (a**2 + b**2)
        x = [a * c / (a**2 + b**2) + b * root_term, a * c / (a**2 + b**2) - b * root_term]
        y = [b * c / (a**2 + b**2) - a * root_term, b * c / (a**2 + b**2) + a * root_term]
        return [Point(x0 + x[0], y0 + y[0]), Point(x0 + x[1], y0 + y[1])]

    except ValueError:
        return []

def _line_line_intersection(line1, line2):
    '''Returns the intersection Point between lines.
       if the lines are parallel or identical, and empty list is returned.'''
    a1, b1, c1 = line1
    a2, b2, c2 = line2

    try:
        x_intersect = (c2 * b1 - b2 * c1) / (a2 * b1 - b2 * a1)

        if abs(b2) > abs(b1):
            y_intersect = (c2 - a2 * x_intersect) / b2
        else:
            y_intersect = (c1 - a1 * x_intersect) / b1
        return [Point(x_intersect, y_intersect)]

    except ZeroDivisionError:
        return []

