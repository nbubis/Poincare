'''Test suite to test functions of the hyperbolic objects.'''

import math

from poincare.hyperbolic.point import HyperbolicPoint
from poincare.hyperbolic.line import HyperbolicLine
from poincare.euclidean.circle import Circle
from poincare.euclidean.point import Point

def test_point():
    '''Test the hyperbolic Point class'''
    e1 = HyperbolicPoint(5.0, 6)
    e2 = HyperbolicPoint(5, 4.0)
    assert e1 + e2 == HyperbolicPoint(10, 10)
    assert e1 * e2 == 49.0
    assert e1 / 4 == HyperbolicPoint(1.25, 1.5)

def test_line():
    '''Test the hyperbolic Line class'''
    p1, p2 = HyperbolicPoint(0.1, -0.5), HyperbolicPoint(0.2, 0.6)
    l1 = HyperbolicLine(p1, p2)
    assert abs(l1.get_representation().center.x - 4.55) < 10e-9
    assert abs(l1.get_representation().center.y + 0.35) < 10e-9

    unit_circle = Circle(Point(0, 0), 1)
    print(l1.get_representation().center, l1.get_representation().radius)
    print('circle intersecion points: ', unit_circle.intersection(l1.get_representation()))
    # print(l1.get_representation().center, l1.get_representation().radius)

    assert abs(unit_circle.angle_between(l1.get_representation()) - math.pi / 2) < 10e-9

if __name__ == '__main__':
    print('Testing HyperbolicPoint class...')
    test_point()
    print('Testing HyperbolicLine class...')
    test_line()
    print('All tests passed successfully.')
