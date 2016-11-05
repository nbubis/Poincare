'''Test suite to test functions of the hyperbolic objects.'''

import math
from hyperbolic import HyperbolicLine, HyperbolicPoint, unit_circle

TEST_THRESHOLD = 10e-12
APPROX_TEST_THRESHOLD = 10e-3

def test_point():
    '''Test the hyperbolic Point class'''
    p1, p2, p3 = HyperbolicPoint(-0.2, 0.4), HyperbolicPoint(0.2, 0.3), HyperbolicPoint(-0.5, 0.1)

    assert abs(math.degrees(HyperbolicPoint.angle_between_three_points(p1, p2, p3)) - 30.35671) < APPROX_TEST_THRESHOLD

    p1 = HyperbolicPoint(0.6, 0.1)
    assert abs(p1.hyperbolic_circle(1).radius - 0.31611) < APPROX_TEST_THRESHOLD

def test_line():
    '''Test the hyperbolic Line class'''
    p1, p2, p3 = HyperbolicPoint(0.1, -0.5), HyperbolicPoint(0.2, 0.6), HyperbolicPoint(0.4, 0.8)
    l1 = HyperbolicLine(p1, p2)
    l2 = HyperbolicLine(p1, p3)

    assert abs(l1.representation().center.x - 4.55) < TEST_THRESHOLD
    assert abs(l1.representation().center.y + 0.35) < TEST_THRESHOLD
    assert abs(unit_circle().angle_between(l1.representation()) - math.pi / 2) < TEST_THRESHOLD
    assert (l1.intersection(l2) - p1).distance_to_origin() < TEST_THRESHOLD

    assert abs(p1.distance(p2) - 2.55828) < APPROX_TEST_THRESHOLD
    assert abs(p1.distance(p3) - 3.91378) < APPROX_TEST_THRESHOLD

if __name__ == '__main__':
    print('Testing HyperbolicPoint class...')
    test_point()
    print('Testing HyperbolicLine class...')
    test_line()
    print('All tests passed successfully.')
