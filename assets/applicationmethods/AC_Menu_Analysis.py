from subprogs.distance_read.Distance_read import DistanceRead
from subprogs.integrate_region.IntegrateRegion import IntegrateRegion
from subprogs.curve_fit.curve_fit import CurveFit

class MenuAnalysisMixin:

    def xy_distance(self):

        ''' Calculate XY Distance'''

        xy_distance = DistanceRead(self, which='first')

    def integrate_region(self):

        ''' Integrate region '''

        integrate_region = IntegrateRegion(self, which='first')

    def curve_fit(self):

        ''' Curve Fit '''

        curve_fit = CurveFit(self, which = 'first')



    