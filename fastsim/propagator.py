from vectors import Point
from math import sqrt, sin

class StraightLinePropagator(object):        
    
    def propagate(self, particle, cylinder):
        udir = particle.p4.Vect().Unit()
        theta = udir.Theta()
        origin = particle.vertex
        if udir.Z():
            destz = cylinder.z if udir.Z() > 0. else -cylinder.z
            length = (destz - origin.Z())/udir.Z()
            assert(length>=0)
            destination = origin + udir * length
            rdest = destination.Perp()
            if rdest > cylinder.rad:
                length -= (rdest-cylinder.rad) / sin(theta)
                destination = origin + udir * length
        particle.points[cylinder.name] = destination

straight_line = StraightLinePropagator()

