
import math
from numbers import Real
from . euclidean import Point, Line, Circle


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
        try:
            return HyperbolicLine(self, other).length()
        except IndexError:
            return 0.0

    def polar_line(self):
        '''Returns the polar line of a point, defined as the locus of all arc centers passing through the point.'''
        return Line(2.0*self.x, 2.0*self.y, 1.0 + self.x**2 + self.y**2)

    @staticmethod
    def angle_between_three_points(point_1, point_2, point_3):
        '''Returns the angle in radians formed between point 1, point 2 and point 3.
           Returned angle will be in between zero and pi.'''
        a, b, c = point_1.distance(point_2), point_2.distance(point_3), point_1.distance(point_3)
        cos_angle = (math.cosh(a) * math.cosh(b) - math.cosh(c)) / math.sinh(a) / math.sinh(b)
        try:
            return math.acos(cos_angle)
        except ValueError:
            if c < a:
                return 0.0
            else:
                return math.pi

    def hyperbolic_circle(self, hyperbolic_radius):
        '''Return a hyperbolic circle, having the prescribed hyperbolic radius and centered around the current point.'''
        euclidean_dist_to_center = self.euclidean_distance_to_origin()
        if euclidean_dist_to_center > 0.0:
            dist_to_near_point = math.tanh(0.5*(2.0 * math.atanh(euclidean_dist_to_center) - hyperbolic_radius))
            dist_to_far_point = math.tanh(0.5*(2.0 * math.atanh(euclidean_dist_to_center) + hyperbolic_radius))
            near_point = self * (dist_to_near_point / euclidean_dist_to_center)
            far_point = self * (dist_to_far_point / euclidean_dist_to_center)
            euclidean_radius = (far_point - near_point).euclidean_distance_to_origin() / 2
            euclidean_center = (far_point + near_point) / 2
        else:
            euclidean_radius = math.tanh(hyperbolic_radius / 2.0)
            euclidean_center = self
        return Circle(euclidean_center, euclidean_radius)


class HyperbolicLine(object):
    '''Class for lines in hyperblic space, as represented by the Poincare Disk Model
       Internally stores objects of the form 'k(x^2 + y^2) - 2 x0 x - 2 y0 y + k', where 'k'' is either 1 or 0.
       the value of 'not k' may be retrieved using the attribute 'is_a_straight_line'.'''

    def __init__(self, point_a, point_b):
        '''Constructs a HyperbolicLine between two Points.'''
        if not point_a.is_in_unit_disk() or not point_b.is_in_unit_disk():
            raise ValueError('Points must be inside the unit disk.')
        self._end_points = [HyperbolicPoint(point_a), HyperbolicPoint(point_b)]
        self._is_a_straight_line = False
        if Line(point_a, point_b).distance_to_origin() < 1e-9:
            self._is_a_straight_line = True
            if point_a.distance_to_origin() > point_b.distance_to_origin():
                self._x0, self._y0 = point_a.y, -point_a.x
            else:
                self._x0, self._y0 = point_b.y, -point_b.x
        else:
            self._x0, self._y0 = point_a.polar_line().intersection(point_b.polar_line())[0]

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
        if p == q:
            return 0.0
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

        # move angle to range [-pi, pi]
        while angle > math.pi:
            angle -= 2*math.pi
        while angle < -math.pi:
            angle += 2*math.pi

        anchor = self.end_points[1]
        polar = anchor.polar_line()
        return_straight_line = False

        if self.is_a_straight_line:
            new_tangent = self.representation().rotated_line(anchor, angle)
            if new_tangent.distance_to_origin() < 1e-12: # our tangent is actually our line
                return_straight_line = True
                candidate_end_points = \
                    [HyperbolicPoint(p) for p in anchor.hyperbolic_circle(length).intersection(new_tangent)]
            else:
                new_center = new_tangent.orthogonal_line_at_point(anchor).intersection(polar)[0]

        if not self.is_a_straight_line:
            pole = self.representation().center
            rotated_line = Line(pole, anchor).rotated_line(anchor, angle)
            new_center = HyperbolicPoint(rotated_line.intersection(polar)[0])

        if not return_straight_line:
            new_radius = Point.distance(anchor, new_center)
            new_arc = Circle(new_center, new_radius)
            candidate_end_points = [HyperbolicPoint(p) for p in anchor.hyperbolic_circle(length).intersection(new_arc)]

        if angle == 0.0:
            dist1, dist2 = [end_point.distance(self.end_points[0]) for end_point in candidate_end_points]
            end_point = candidate_end_points[0] if dist1 > dist2 else candidate_end_points[1]
            return HyperbolicLine(anchor, end_point)

        
        for end_point in candidate_end_points:
            formed_angle = HyperbolicPoint.angle_between_three_points(self.end_points[0], self.end_points[1], end_point)
            if abs(formed_angle + abs(angle) - math.pi) < 1.0e-5:
                return HyperbolicLine(anchor, end_point)
                