'''Test suite to test functions of the euclidean objects.'''

import math
import itertools

from euclidean import Point, Line, Circle

TEST_THRESHOLD = 10e-12
APPROX_TEST_THRESHOLD = 10e-3

def test_point():
    '''Test the euclidean Point class'''
    p1, p2 = Point(5.0, 6), Point(5, 4.0)
    assert (p1 + p2 - Point(10, 10)).distance_to_origin() < TEST_THRESHOLD
    assert abs(p1 * p2 - 49.0) < TEST_THRESHOLD
    assert (p1 / 4 - Point(1.25, 1.5)).distance_to_origin() < TEST_THRESHOLD
    assert (p1.rotated_point(p2, math.pi / 2) - Point(3, 4)).distance_to_origin() < TEST_THRESHOLD

def test_line():
    '''Test the euclidean Line class'''
    p1, p2 = Point(0, 0), Point(0, 5)
    l1 = Line(p1, p2)
    l2 = l1.orthogonal_line_at_point(p2)
    assert (l2.intersection(l1)[0] - p2).distance_to_origin() < TEST_THRESHOLD
    assert abs(l1.angle_between(l2)*2 - math.pi) < TEST_THRESHOLD

    p3 = Point(1, 1)
    rotated_line = l1.rotated_line(p3, math.pi / 6)
    assert (rotated_line.intersection(l1)[0] - Point(0.0, 0.732)).distance_to_origin() < APPROX_TEST_THRESHOLD

def test_circle():
    '''Test the euclidean Circle class'''
    p1, p2, p3 = Point(1, 1), Point(2, 4), Point(5, 3)
    circle = Circle.create_from_three_points(p1, p2, p3)
    assert circle.center == Point(3, 2)
    assert abs(circle.radius**2 - 5.0) < TEST_THRESHOLD

    circle1, circle2 = Circle(Point(-0.5, 0), 1), Circle(Point(0.5, 0), 1)
    assert abs(circle1.intersection(circle2)[0].y**2 - 0.75) < TEST_THRESHOLD
    assert abs(circle1.angle_between(circle2) * 180 / math.pi - 60) < TEST_THRESHOLD

    line = Line(5, 8, 40)
    circle = Circle(Point(4, 3), 3)
    approx_intersection_points = [Point(x=6.294, y=1.067), Point(x=1.257, y=4.214)]
    intersection_points = circle.intersection(line)

    true_conditions = [[False]*2 for i in range(2)]
    for i, j in itertools.product(range(2), range(2)):
        true_conditions[i][j] += \
            int(approx_intersection_points[i].distance(intersection_points[j]) < APPROX_TEST_THRESHOLD)
    assert (true_conditions[0][0] and true_conditions[1][1]) or (true_conditions[0][1] and true_conditions[1][0])

if __name__ == '__main__':
    print('Testing euclidean Point class...')
    test_point()
    print('Testing euclidean Line class...')
    test_line()
    print('Testing euclidean Circle class...')
    test_circle()
    print('All tests passed successfully.')
