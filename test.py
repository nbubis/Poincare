
from math import sin, cos, tan, acosh, pi, tanh
from poincare import HyperbolicLine, HyperbolicPoint
from poincare.poincaredisk import PoincareDiskModel


def create_stellated_star_lines(baseline, side_num, theta, rotation=0):
    '''Returns a list of hyperbolic lines creating a stellated star.
       baseline - Hyperbolic line starting at one corner and ending at the center
       side_num - The number of sides in the star
       theta    - The angle of stellation, smaller angles give more accute angles.
       rotation - Allows rotation of the star relative to the original baseline.
    '''
    radii = []
    for i in range(side_num):
        radii.append(baseline.line_at_angle(2 * i * pi / side_num + rotation, baseline.length()))

    stellations = []
    for i in range(side_num):
        stellations.append(radii[i].line_at_angle(pi - theta, 5))
        stellations.append(radii[(i + 1) % side_num].line_at_angle(pi + theta, 5))

    stellation_lines = []
    for i in range(side_num):
        stellation_intersection1 = stellations[2*i].intersection(stellations[(2*i + 1) % (2 * side_num)])
        stellation_intersection2 = stellations[2*i].intersection(stellations[(2*i + 3) % (2 * side_num)])

        stellation_lines += [HyperbolicLine(stellation_intersection1, radii[i].end_points[1]),
                             HyperbolicLine(stellation_intersection1, radii[(i + 1) % side_num].end_points[1]),
                             HyperbolicLine(stellation_intersection2, radii[i].end_points[1]),
                             HyperbolicLine(stellation_intersection2, radii[(i + 2) % side_num].end_points[1])]
    return stellation_lines


def draw_hyperbolic_rosette(poincare_disk_model, major_side_num, minor_side_num, theta):
    '''Draws our hyperbolic islamic rosette pattern, with a "major" star surrounded by "minor" stars.
       poincare_disk_model - A PoincareDiskModel object to draw on
       major_side_num      - The number of sides for the "major" centeral star
       minor_side_num      - The number of sides for the "minor" surrounding stars
       theta               - The angle of stellation, smaller angles give more accute angles.
    '''

    pdm = poincare_disk_model

    # First we find the radii of the bounding circles

    minor_radius_length = acosh(cos(pi / major_side_num) / sin(2 * pi / minor_side_num))
    major_radius_length = acosh(1 / tan(pi / major_side_num) / tan(2 * pi / minor_side_num)) - minor_radius_length

    baseline = HyperbolicLine(HyperbolicPoint(tanh(major_radius_length / 2.0), 0), HyperbolicPoint(0, 0))

    # Draw major star

    for line in create_stellated_star_lines(baseline, major_side_num, theta):
        pdm.drawline(line)

    # Find locations of minor stars

    for i in range(major_side_num):
        center_angle = 2 * i * pi / major_side_num
        minor_center = baseline.line_at_angle(center_angle, major_radius_length + minor_radius_length).end_points[1]
        minor_radius = baseline.line_at_angle(center_angle, major_radius_length).end_points[1]
        minor_baseline = HyperbolicLine(minor_radius, minor_center)

        # Draw minor star

        for line in create_stellated_star_lines(minor_baseline, minor_side_num, theta, pi / minor_side_num):
            pdm.drawline(line)

    pdm.show()


if __name__ == '__main__':
    draw_hyperbolic_rosette(PoincareDiskModel(), 9, 9, pi / 10)
