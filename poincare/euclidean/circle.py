
import math
from poincare.euclidean.point import Point
from poincare.euclidean.line import Line

class Circle(object):
    '''Class for euclidean circle objects.'''

    def __init__(self, center, radius):
        '''Constructs a Circle using a center Point and the radius.'''
        self.center, self.radius = center, radius

    def _circle_intersection(self, other):
        '''Returns list of intersection points between the circle and circles.'''
        x0, y0, r0 = self.center.x, self.center.y, self.radius
        x1, y1, r1 = other.center.x, other.center.y, other.radius

        center_distance_sq = (x0 - x1)**2 + (y0 - y1)**2
        x_intersection_first_term = 0.5 * (x0 + x1) + 0.5 * (x0 - x1)*(r1**2 - r0**2) / center_distance_sq
        y_intersection_first_term = 0.5 * (y0 + y1) + 0.5 * (y0 - y1)*(r1**2 - r0**2) / center_distance_sq

        x_intersection_second_term = 0.5 * (y1 - y0) / center_distance_sq * \
            math.sqrt(((r1 + r0)**2 - center_distance_sq) * (center_distance_sq - (r1 - r0)**2))
        y_intersection_second_term = 0.5 * (x1 - x0) / center_distance_sq * \
            math.sqrt(((r1 + r0)**2 - center_distance_sq) * (center_distance_sq - (r1 - r0)**2))
        point1 = Point(x_intersection_first_term + x_intersection_second_term,
                       y_intersection_first_term - y_intersection_second_term)
        point2 = Point(x_intersection_first_term - x_intersection_second_term,
                       y_intersection_first_term + y_intersection_second_term)
        return [point1, point2]

    def _line_intersection(self, other):
        '''Returns list of intersection points between the circle and other lines.'''
        x0, y0, r0 = self.center.x, self.center.y, self.radius
        a, b, c = other.a, other.b, other.c
        c = c - a * x0 - b * y0
        root_term = math.sqrt(r0**2 * (a**2 + b**2) - c**2) / (a**2 + b**2)
        x = [a * c / (a**2 + b**2) + b * root_term, a * c / (a**2 + b**2) - b * root_term]
        y = [b * c / (a**2 + b**2) - a * root_term, b * c / (a**2 + b**2) + a * root_term]
        return [Point(x0 + x[0], y0 + y[0]), Point(x0 + x[1], y0 + y[1])]

    def intersection(self, other):
        '''Returns list of intersection points between the circle and other lines or circles.'''

        if isinstance(other, Line):
            return self._line_intersection(other)
        elif isinstance(other, Circle):
            return self._circle_intersection(other)
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

        if not isinstance(other, Circle):
            raise NotImplementedError

        intersection_pt = self.intersection(other)[0]
        lines_to_centers = [Line(intersection_pt, self.center), Line(intersection_pt, other.center)]
        return lines_to_centers[0].angle_between(lines_to_centers[1])
