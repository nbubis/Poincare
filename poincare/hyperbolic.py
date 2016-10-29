
import math
from numbers import Real
from scipy.optimize import minimize_scalar
from euclidean import Point, Line, Circle


def unit_circle():
    '''Returns the unit circle, the representation of the Poincare Disk.'''
    return Circle(Point(0, 0), 1)

class HyperbolicPoint(Point):
    '''Class for points on the Poincare disk inheriting from the euclidean Point class.'''

    def __new__(cls, *kargs):
        if len(kargs) == 2 and all(isinstance(i, Real) for i in kargs):
            return super().__new__(cls, kargs[0], kargs[1])
        elif len(kargs) == 1 and all(isinstance(i, Point) for i in kargs):
            return super().__new__(cls, kargs[0].x, kargs[0].y)
        else:
            raise NotImplementedError

    def euclidean_distance_to_origin(self):
        '''Euclidean distance to the origin of the Poincare Disk.'''
        return Point.distance_to_origin(self)

    def inverse(self):
        '''Inverse point in respect with the Poincare Disk.'''
        distance = self.euclidean_distance_to_origin()
        return HyperbolicPoint(self.x / distance**2, self.y / distance**2)

    def distance_to_origin(self):
        '''Hyperbolic distance to the origin.'''
        return 2.0 * math.atanh(self.euclidean_distance_to_origin())

    def is_in_unit_disk(self):
        '''Checks if point is actually in the Poincare Disc'''
        return self.euclidean_distance_to_origin() < 1.0

    def distance(self, other):
        '''Returns the hyperbolic distance between two points in the Poincare Disk.'''
        return HyperbolicLine(self, other).length()

    def polar_line(self):
        '''Returns the polar line of a point, defined as the locus of all arc centers passing through the point.'''
        return Line(2.0*self.x, 2.0*self.y, 1.0 + self.x**2 + self.y**2)


class HyperbolicLine(object):
    '''Class for lines in hyperblic space, as represented by the Poincare Disk Model
       Internally stores objects of the form 'k(x^2 + y^2) - 2 x0 x - 2 y0 y + k', where 'k'' is either 1 or 0.
       the value of 'not k' may be retrieved using the attribute 'is_a_straight_line'.'''

    def __init__(self, point_a, point_b):
        '''Constructs a HyperbolicLine between two Points.'''
        if not point_a.is_in_unit_disk() or not point_b.is_in_unit_disk():
            raise ValueError('Points must be inside the unit disk.')
        self._end_points = [point_a, point_b]
        self._is_a_straight_line = False

        try:
            self._x0, self._y0 = point_a.polar_line().intersection(point_b.polar_line())[0]
        except IndexError:
            self._is_a_straight_line = True

            if point_a.distance_to_origin() > point_b.distance_to_origin():
                self._x0, self._y0 = point_a.y, -point_a.x
            else:
                self._x0, self._y0 = point_b.y, -point_b.x

    @property
    def is_a_straight_line(self):
        '''Returns if the hyperbolic line is a also an euclidean stright line passing through the origin.'''
        return self._is_a_straight_line
    @property
    def end_points(self):
        '''Get end points defining the line.'''
        return self._end_points

    def length(self):
        '''Return hyperbolic length of line as defined by it's end points.'''
        p, q = self.end_points
        a, b = self.representation().intersection(unit_circle())
        if Point.distance(a, q) < Point.distance(a, p):
            a, b = b, a
        ratio = (Point.distance(a, q) * Point.distance(p, b)) / (Point.distance(a, p) * Point.distance(q, b))
        return math.log(ratio)

    def representation(self):
        '''Get arc representation as either a circle or a line.'''
        if self._is_a_straight_line:
            return Line(self._x0, self._y0, 0)
        else:
            radius = math.sqrt(self._x0**2 + self._y0**2 - 1.0)
            return Circle(Point(self._x0, self._y0), radius)

    def intersection(self, other):
        '''Return intersection point between hyperbolic lines.
           Returns 'None' if no intersection is found.'''

        intersection_points = self.representation().intersection(other.representation())
        if isinstance(intersection_points, list):
            for intersection_point in intersection_points:
                if HyperbolicPoint(intersection_point).is_in_unit_disk():
                    return HyperbolicPoint(intersection_point)
            return None
        else:
            return HyperbolicPoint(intersection_points)

    def line_at_angle(self, angle, length):
        '''Returns a line starting from the end point of the current line, having the prescribed length,
           and meeting the existing line at the specified angle.'''
        anchor = self._end_points[1]
        polar = anchor.polar_line()
        if not self.is_a_straight_line:
            pole = self.representation().center
            line = Line(pole, anchor)
            rotated_line = line.rotated_line(anchor, angle)
            new_center = rotated_line.intersection(polar)
            radius = Point.distance(self, new_center)
            initial_azimuth = (anchor - new_center).azimuth()
            Circle(new_center, radius).intersection(unit_circle())

            def length_diff(end_angle):
                p = new_center + HyperbolicPoint(radius * math.cos(end_angle), radius * math.sin(end_angle))
                if not p.is_in_unit_disk():
                    return float("inf")
                return p.distance(anchor) - length

            end_angle = minimize_scalar(
                length_diff, bracket=[initial_azimuth, 2 * math.pi], method='golden', tol=1.0e-12).x
            end_point = new_center + HyperbolicPoint(radius * math.cos(end_angle), radius * math.sin(end_angle))
            return HyperbolicLine(anchor, end_point)
        return None

