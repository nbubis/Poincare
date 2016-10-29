'''Test suite to test functions of the hyperbolic objects.'''

import math
from hyperbolic import HyperbolicLine, HyperbolicPoint, unit_circle

TEST_THRESHOLD = 10e-12

def test_point():
    '''Test the hyperbolic Point class'''
    e1 = HyperbolicPoint(5.0, 6)
    e2 = HyperbolicPoint(5, 4.0)
    assert (e1 + e2 - HyperbolicPoint(10, 10)).euclidean_distance_to_origin() < TEST_THRESHOLD
    assert abs(e1 * e2 - 49.0) < TEST_THRESHOLD
    assert (e1 / 4 - HyperbolicPoint(1.25, 1.5)).euclidean_distance_to_origin() < TEST_THRESHOLD

def test_line():
    '''Test the hyperbolic Line class'''
    p1, p2, p3 = HyperbolicPoint(0.1, -0.5), HyperbolicPoint(0.2, 0.6), HyperbolicPoint(0.4, 0.8)
    l1 = HyperbolicLine(p1, p2)
    l2 = HyperbolicLine(p1, p3)

    assert abs(l1.representation().center.x - 4.55) < TEST_THRESHOLD
    assert abs(l1.representation().center.y + 0.35) < TEST_THRESHOLD
    assert abs(unit_circle().angle_between(l1.representation()) - math.pi / 2) < TEST_THRESHOLD
    assert (l1.intersection(l2) - p1).distance_to_origin() < TEST_THRESHOLD

    p1, p2 = HyperbolicPoint(0.0, 0.0), HyperbolicPoint(0.99, 0.0001)
    l1 = HyperbolicLine(p1, p2)
    assert l1.is_a_straight_line

if __name__ == '__main__':
    print('Testing HyperbolicPoint class...')
    test_point()
    print('Testing HyperbolicLine class...')
    test_line()
    print('All tests passed successfully.')
