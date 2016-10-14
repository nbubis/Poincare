
import math
from poincare.euclidean.point import Point

class HyperbolicPoint(Point):
    '''Class for points on the Poincare disk inheriting from the euclidean Point class.'''

    def euclidean_distance_to_origin(self):
        '''Euclidean distance to the origin of the Poincare Disk.'''
        return Point.distance_to_origin(self)

    def inverse(self):
        '''Inverse point in respect with the Poincare Disk.'''
        distance = self.euclidean_distance_to_origin()
        return HyperbolicPoint(self.x / distance**2, self.y / distance**2)

    def distance_to_origin(self):
        '''Hyperbolic distance to the origin.'''
        return 2.0 * math.atanh(self.euclidean_distance_to_origin())

    def isvalid(self):
        '''Checks if point is actually in the Poincare Disc'''
        return self.euclidean_distance_to_origin() < 1.0
