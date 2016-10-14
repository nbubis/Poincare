from __future__ import division
import math
from numbers import Real
from collections import namedtuple
import bokeh.plotting

class HyperbolicPoint(Point):
    '''Class for points on the Poincare disk'''

    @property
    def unit_circle(self):
        return Circle(Point(0.0, 0.0), 1.0)

    def euclidean_distance_to_origin(self):
        return Point.distance_to_origin(self)

    def inverse(self):
        distance = self.euclidean_distance_to_origin()
        return Point(self.x / distance**2, self.y / distance**2)

    def distance_to_origin(self):
        return 2.0 * math.atanh(self.euclidean_distance_to_origin())

    def arc_to_point(self, other):
        point_c = self.inverse()
        return Circle.create_from_three_points(self, other, point_c)

    def distance(self, other):
        if isinstance(other, HyperbolicPoint):
            if Point.distance(self, other) < 10e-9:
                return 0.0
            if abs(Line(self, other).distance_to_point(Point(0, 0))) < 10e-9:
                return abs(self.distance_to_origin() - other.distance_to_origin())

            arc_circle = self.arc_to_point(other)
            p, q = self, other
            a, b = arc_circle.intersection(self.unit_circle)
            if Point.distance(a, q) < Point.distance(a, p):
                a, b = b, a
            ratio = (Point.distance(a, q) * Point.distance(p, b)) / (Point.distance(a, p) * Point.distance(q, b))
            return math.log(ratio)

        else:
            raise NotImplementedError

    def __add__(self, other):
        return HyperbolicPoint(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return HyperbolicPoint(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, HyperbolicPoint):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Real):
            return HyperbolicPoint(self.x * other, self.y * other)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Real):
            return HyperbolicPoint(self.x / other, self.y / other)
        else:
            raise NotImplementedError

class PoincareDiskModel():
    def __init__(self):
        self._plot = bokeh.plotting.figure(plot_width=600, plot_height=600, min_border=100,
                                           x_range=(-1, 1), y_range=(-1, 1), tools='', logo=None)
        theta_range = [0.02 * math.pi * x for x in range(101)]
        x = [math.cos(th) for th in theta_range]
        y = [math.sin(th) for th in theta_range]
        self._plot.line(x, y)

    def draw_point(self, point):
        self._plot.circle(point.x, point.y)

    def draw_arc(self, point_a, point_b):
        arc = point_a.arc_to_point(point_b)
        theta1 = (point_a - arc.center).azimuth()
        theta2 = (point_b - arc.center).azimuth()
        theta_range = [theta1 + 0.01 * (theta2 - theta1) * x for x in range(101)]
        x = [arc.center.x + arc.radius * math.cos(th) for th in theta_range]
        y = [arc.center.y + arc.radius * math.sin(th) for th in theta_range]
        self._plot.line(x, y)

    def show(self):

        bokeh.plotting.show(self._plot)


def main():
    from scipy.optimize import minimize_scalar

    major_side_num, minor_side_num = 7, 7
    sin_value = math.sin(math.pi / major_side_num)
    cos_value = math.cos(2.0 * math.pi / minor_side_num)

    def cos_value_from_length(total_length):
        return abs(math.tanh(math.asinh(sin_value * math.sinh(total_length))) / math.tanh(total_length) - cos_value)

    total_length = minimize_scalar(cos_value_from_length, bracket=[0.01, 3], method='golden', tol=1.0e-12).x

    minor_length = math.asinh(sin_value * (math.sinh(total_length)))
    major_length = total_length - minor_length
    print major_length, minor_length

    major_euclidean_distance = math.tanh(major_length / 2.0)
    total_euclidean_distance = math.tanh(total_length / 2.0)

    pdm = PoincareDiskModel()

    major_polygon_corners = []
    minor_polygon_centers = []
    for i in range(major_side_num):
        theta = i * 2.0 * math.pi / major_side_num
        major_polygon_corners.append(major_euclidean_distance * HyperbolicPoint(math.cos(theta), math.sin(theta)))
        minor_polygon_centers.append(total_euclidean_distance * HyperbolicPoint(math.cos(theta), math.sin(theta)))

    for i in range(major_side_num):
        pdm.draw_point(minor_polygon_centers[i])
        pdm.draw_point(major_polygon_corners[i])


    A = major_polygon_corners[0]
    C = minor_polygon_centers[0]
    M = (major_polygon_corners[0] + major_polygon_corners[1]) / 3.0
    pdm._plot.circle(A.x, A.y, color='#FF00F0')
    pdm._plot.circle(M.x, M.y, color='#FF000F')
    pdm._plot.circle(C.x, C.y, color='#F000FF')

    AM = A.arc_to_point(M)

    def angle_diff(theta):
        X = AM.center + AM.radius * HyperbolicPoint(math.cos(theta), math.sin(theta))
        X = HyperbolicPoint(X.x, X.y)
        XC = X.arc_to_point(C)
        
        line_angle = Line(XC.center, C).orthogonal_line_at_point(C).angle_between(Line(C, A))
        temp = minor_side_num / math.pi - line_angle
        if temp > math.pi / 2:
            return temp - math.pi / 2
        return temp

    theta1 = (A - AM.center).azimuth() + 1.0e-9
    theta2 = (C - AM.center).azimuth() - 1.0e-9

    theta = minimize_scalar(angle_diff, bracket=[theta2, theta1], method='golden', tol=1.0e-12).x
    print theta
            # if theta1 > theta2: 
            #     theta1, theta2 = theta2, theta1 
            # # print theta1, theta2, angle_diff(theta1), angle_diff(theta2) 
            # error = 1.0
            # # for k in range(10):
            # #     theta = theta1 + k * (theta2 - theta1) / 10.0
            # #     print angle_diff(theta)
            # theta = theta1 + 10.0e-9
            # #     theta1 = math.pi / 2
            # # theta = theta1 + 1.0e-9
            # # print error
            # N = 0
            # while error > 1.0e-3:
            #     derivative = (angle_diff(theta + 1.0e-8) - angle_diff(theta)) / 1.0e-8
            #     theta = theta - 0.0000001 * derivative
            #     error = abs(angle_diff(theta))
            #     print theta, error
            #     N += 1
            #     if (N > 1000000): break
            # X = AM.center + AM.radius * HyperbolicPoint(math.cos(theta), math.sin(theta))
            # X = HyperbolicPoint(X.x, X.y)

            # # # pdm._plot.circle(X.x, X.y, color='#0000F0')
            # pdm.draw_arc(X, C)
            # pdm.draw_arc(X, M)
    # pdm.show()



if __name__ == '__main__':
    main()
