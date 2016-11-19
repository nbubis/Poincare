
import math
import bokeh.plotting

from . hyperbolic import HyperbolicLine, HyperbolicPoint

class PoincareDiskModel():
    def __init__(self):
        self._plot = bokeh.plotting.figure(plot_width=600, plot_height=600, min_border=50,
                                           x_range=(-1, 1), y_range=(-1, 1), tools=['zoom_in', 'zoom_out'], logo=None)
        self._plot.arc(x=0.0, y=0.0, radius=1.0, start_angle=0.0, end_angle=2.0*math.pi)

    def drawpoint(self, point, **kwargs):
        self._plot.circle(point.x, point.y, **kwargs)

    def drawline(self, hyperbolic_line, **kwargs):
        if hyperbolic_line.is_a_straight_line:
            self._plot.line(x=[hyperbolic_line.end_points[i].x for i in range(2)],
                            y=[hyperbolic_line.end_points[i].y for i in range(2)], **kwargs)
        else:
            circle = hyperbolic_line.representation()
            start_angle = (hyperbolic_line.end_points[0] - circle.center).azimuth()
            end_angle = (hyperbolic_line.end_points[1] - circle.center).azimuth()
            start_angle, end_angle = [angle if angle > 0 else angle + 2*math.pi for angle in [start_angle, end_angle]]
            start_angle, end_angle = min(start_angle, end_angle), max(start_angle, end_angle)
            if abs(end_angle - start_angle) > math.pi:
                start_angle, end_angle = end_angle, start_angle

            self._plot.arc(x=hyperbolic_line.representation().center.x,
                           y=hyperbolic_line.representation().center.y,
                           radius=hyperbolic_line.representation().radius,
                           start_angle=start_angle, end_angle=end_angle, **kwargs)

    def show(self):
        bokeh.plotting.show(self._plot)

    def save(self, filename):
        bokeh.plotting.save(obj=self._plot, filename=filename)

