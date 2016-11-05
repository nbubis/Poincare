
import math
from poincare import HyperbolicLine, HyperbolicPoint
from poincare.poincaredisk import PoincareDiskModel
from scipy.optimize import minimize_scalar

def main():

    major_side_num, minor_side_num = 7, 7
    sin_value = math.sin(math.pi / major_side_num)
    cos_value = math.cos(2.0 * math.pi / minor_side_num)

    def cos_value_from_length(total_length):
        return abs(math.tanh(math.asinh(sin_value * math.sinh(total_length))) / math.tanh(total_length) - cos_value)

    total_length = minimize_scalar(cos_value_from_length, bracket=[0.01, 3], method='golden', tol=1.0e-12).x
    minor_length = math.asinh(sin_value * (math.sinh(total_length)))
    major_length = total_length - minor_length
    print(major_length, minor_length)

    # baseline = HyperbolicLine(HyperbolicPoint(-1, 0), HyperbolicPoint(0,0))
    major_euclidean_distance = math.tanh(major_length / 2.0)
    total_euclidean_distance = math.tanh(total_length / 2.0)

    pdm = PoincareDiskModel()

    major_polygon_corners = []
    minor_polygon_centers = []

    for i in range(major_side_num):
        theta = i * 2.0 * math.pi / major_side_num
        major_polygon_corners.append(major_euclidean_distance * HyperbolicPoint(math.cos(theta), math.sin(theta)))
        minor_polygon_centers.append(total_euclidean_distance * HyperbolicPoint(math.cos(theta), math.sin(theta)))

    major_midpoints = []
    for i in range(major_side_num):
        major_midpoints.append((major_polygon_corners[i] + major_polygon_corners[(i + 1) % major_side_num]) / 4.0)

    for i in range(major_side_num):
        pdm.drawpoint(minor_polygon_centers[i])
        pdm.drawpoint(major_polygon_corners[i])
        pdm.drawpoint(major_midpoints[i])

    for i in range(major_side_num):
        l1 = HyperbolicLine(major_midpoints[i], major_polygon_corners[i])
        l2 = HyperbolicLine(major_midpoints[i], major_polygon_corners[(i + 1) % major_side_num])
        pdm.drawline(l1)
        pdm.drawline(l2)

        pdm.drawline(l1.line_at_angle(0.000, 1))
        pdm.drawline(l2.line_at_angle(0.000, 1))

    pdm.show()



if __name__ == '__main__':
    main()
