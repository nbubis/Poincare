'''Test suite to test functions of the euclidean objects.'''

import math
import itertools

from poincare.euclidean.point import Point
from poincare.euclidean.line import Line
from poincare.euclidean.circle import Circle

def test_point():
    '''Test the euclidean Point class'''
    e1 = Point(5.0, 6)
    e2 = Point(5, 4.0)
    assert e1 + e2 == Point(10, 10)
    assert e1 * e2 == 49.0
    assert e1 / 4 == Point(1.25, 1.5)

def test_line():
    '''Test the euclidean Line class'''
    p1, p2 = Point(0, 0), Point(0, 5)
    l1 = Line(p1, p2)
    l2 = l1.orthogonal_line_at_point(p2)
    assert l2.intersection(l1) == p2
    assert abs(l1.angle_between(l2)*2 - math.pi) < 10e-9

def test_circle():
    '''Test the euclidean Circle class'''
    p1, p2, p3 = Point(1, 1), Point(2, 4), Point(5, 3)
    circle = Circle.create_from_three_points(p1, p2, p3)
    assert circle.center == Point(3, 2)
    assert abs(circle.radius**2 - 5.0) < 10e-9

    circle1, circle2 = Circle(Point(-0.5, 0), 1), Circle(Point(0.5, 0), 1)
    assert abs(circle1.intersection(circle2)[0].y**2 - 0.75) < 10e-9
    assert abs(circle1.angle_between(circle2) * 180 / math.pi - 60) < 10e-9

    line = Line(5, 8, 40)
    circle = Circle(Point(4, 3), 3)
    approx_intersection_points = [Point(x=6.294, y=1.067), Point(x=1.257, y=4.214)]
    intersection_points = circle.intersection(line)

    true_conditions = 0
    for i, j in itertools.product(range(2), range(2)):
        true_conditions += int(approx_intersection_points[i].distance(intersection_points[j]) < 10e-3)
    assert true_conditions == 2

if __name__ == '__main__':
    print('Testing euclidean Point class...')
    test_point()
    print('Testing euclidean Line class...')
    test_line()
    print('Testing euclidean Circle class...')
    test_circle()
    print('All tests passed successfully.')
